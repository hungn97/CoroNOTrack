from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import json
import sqlite3
import textwrap
import os
import time
import socket
import ssl
import pprint
from pathlib import Path


with sqlite3.connect("doctor_database.db") as db:
    cursor = db.cursor()

with open("askey.txt", "rb") as fo:
    # Key for encryption/decryption of auth database
    dataKey = fo.read()
auth_key = Fernet(dataKey)

# Key for encrypting ticket
ticket_key_file = open("ticketkey.txt","r")
ticket_key = ticket_key_file.read().encode()
ticket_key_file.close()
fernet_ticket = Fernet(ticket_key)

# Key for signing nonce
with open("priv_key.pem", "rb") as key_file:
    server_private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

TIMEOUT = 5  # minutes
user_public_key = None


# MIGHT NOT NEED BECAUSE OF SSL
# def decrypt_message(message):
#     """Takes in an AES encrypted message and returns a decrypted json object"""
#
#
# def encrypt_message(message):
#     """Takes in a plaintext message and returns an AES encrypted object"""


def verify_timestamp(timestamp):
    """Takes in a timestamp to check if message is still valid and returns a boolean"""
    if (time.time() - timestamp) < TIMEOUT:
        return True
    else:
        return False


def verify_auth(auth):
    """Takes in a json containing user id and password, hash them, compare hash to
    auth database and return a public key or boolean if false"""
    user_id = auth["user_id"]
    user_pw = auth["user_pw"]
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(user_pw.encode())
    hashed_pw = pw_hash_func.finalize()
    find_user = "SELECT * FROM user WHERE user_id = ? AND user_pw = ?"
    cursor.execute(find_user, [user_id, hashed_pw])
    results = cursor.fetchall()

    print("results " + str(results))

    # if auth matches, return the role and public key
    public_key = auth_key.decrypt(results[3])
    if results:
        return user_id, results[2], public_key
    else:
        return False


# def verify_signature(signature):
#     """Takes in a signed object and compares to values previously sent to client and returns a boolean"""


def receive_message_1(message):
    """Takes in the entire message after the initial key exchange from
    the user and returns a session key, nonce tuple or boolean if false"""
    json_plaintext = message
    nonce_1 = json_plaintext["nonce"]
    verified_auth = verify_auth(json_plaintext["auth"])    # user_id, role, pub_key
    print("verified auth" + str(verified_auth))
    if verified_auth:
        return verified_auth[0], verified_auth[1], verified_auth[2], nonce_1
    else:
        return False


def create_ticket(user_id, role):
    """Takes in a user id and returns an encrypted json ticket"""
    ticket = {
        "user_id": user_id,
        "role": role,
        "timestamp": time.time()
    }
    # NEED TO MAKE SURE USER HAS AUTH SERVER PUBLIC KEY
    encrypted_ticket = fernet_ticket.encrypt(ticket)
    return encrypted_ticket


def create_message_1(nonce, timestamp):
    """Takes in a nonce from client's original message and returns a json object
     with a signed nonce 1 and plaintext nonce 2 and timestamp"""
    encrypted_nonce_1 = server_private_key.encrypt(nonce)
    nonce_2 = os.urandom(16).decode('latin1')
    message = {
        "nonce_1": encrypted_nonce_1,
        "nonce_2": nonce_2,
        "timestamp": timestamp
    }
    return message


def receive_message_2(message):
    """Takes in the entire message containing the user signed nonce 2 and timestamp and returns a boolean if valid"""
    # fetch users public key from auth database
    data_json = {
        "nonce": message["nonce"],
        "timestamp": message["timestamp"]
    }
    if not verify_timestamp(message["timestamp"]):
        return None

    serialized_json = json.dumps(data_json)
    byte_json = serialized_json.encode()
    match = True
    try:
        user_public_key.verify(
            message["signature"],
            byte_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
    except:
        match = False
    return match


def create_message_2(user_id, role):
    """Takes in a user id and role and combines with timestamp and returns an encrypted ticket"""
    # might change later if useless

    ticket = create_ticket(user_id, role)
    return ticket



if __name__ == '__main__':
    print("auth server starting")
    HOST = '127.0.0.1'
    PORT = 1234
    cwd_path = Path.cwd()
    certs_path = str(cwd_path) + r"\sslsockets_commit"

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        client, fromaddr = server_socket.accept()
        secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs=(certs_path+r"\client.pem"),
                                      certfile=(certs_path+r"\server.pem"),
                                      keyfile=(certs_path+r"\server.key"),
                                      cert_reqs=ssl.CERT_REQUIRED,
                                      ssl_version=ssl.PROTOCOL_TLSv1_2)
        cert = secure_sock.getpeercert()
        response = 'acknowledge from server'

        print("client connected: " + str(fromaddr))

        try:
            data_in_1 = secure_sock.read(1024)
            print("data in 1" + data_in_1.decode('latin1'))
            try:
                bytes_in_1 = json.loads(data_in_1.decode('latin1'))
                #print("bytes in 1" + str(bytes_in_1))
                message_in_1 = receive_message_1(bytes_in_1)  # user_id, role, pub_key, nonce_1
                #print("message_in_1" + str(message_in_1))
                user_public_key = message_in_1[1]
            except:
                message_in_1 = None
            if message_in_1 is None:
                # invalid auth
                message_out_1 = "Invalid Auth"
                bytes_out_1 = message_out_1.encode()
                secure_sock.write(bytes_out_1)
            else:
                timestamp = time.time()
                message_out_1 = create_message_1(message_in_1[2], timestamp)
                bytes_out_1 = json.dumps(message_out_1).encode()
                secure_sock.write(bytes_out_1)
                # send message

                # receive message
                data_in_2 = secure_sock.read(1024)
                bytes_in_2 = json.loads(data_in_2.decode())
                message_in_2 = receive_message_2(bytes_in_2)
                if message_in_2 is None:
                    # time expired
                    message_out_2 = "Timed out"
                    bytes_out_2 = message_out_2.encode()
                    secure_sock.write(bytes_out_2)
                elif not message_in_2:
                    # bad signature
                    message_out_2 = "Invalid response"
                    bytes_out_2 = message_out_2.encode()
                    secure_sock.write(bytes_out_2)
                else:
                    # success
                    message_out_2 = create_message_2(message_in_1[0], message_in_1[1])
                    bytes_out_2 = message_out_2.encode()
                    secure_sock.write(bytes_out_2)

        finally:
            secure_sock.close()
            server_socket.close()
