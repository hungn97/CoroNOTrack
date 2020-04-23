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
import pickle
from pathlib import Path


with sqlite3.connect("user_database.db") as db:
    cursor = db.cursor()

with open("askey.txt", "rb") as fo:
    # Key for encryption/decryption of auth database
    dataKey = fo.read()
auth_key = Fernet(dataKey)

# Key for encrypting ticket
ticket_key_file = open("ticketkey.txt","r")
ticket_key = ticket_key_file.read().encode('latin1')
ticket_key_file.close()
fernet_ticket = Fernet(ticket_key)

# Key for signing nonce
with open("auth_priv_key.pem", "rb") as key_file:
    server_private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# with open("user_pub_key.pem", "rb") as key_file:
#     user_public_key = serialization.load_pem_public_key(
#         key_file.read(),
#         default_backend()
#     )

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
    pw_hash_func.update(user_pw.encode('latin1'))
    hashed_pw = pw_hash_func.finalize()

    # print("userid " + user_id)
    # print(user_pw)

    find_user = "SELECT * FROM user WHERE user_id = ? AND user_pw = ?"
    cursor.execute(find_user, [user_id, hashed_pw])
    results = cursor.fetchone()
    print("results")
    print(results[3])

    # if auth matches, return the role and public key

    public_key = auth_key.decrypt(results[3])
    print(public_key)
    if results:
        return user_id, results[2], public_key
    else:
        return False


# def verify_signature(signature):
#     """Takes in a signed object and compares to values previously sent to client and returns a boolean"""


def receive_message_1(message):
    """Takes in the entire message after the initial key exchange from
    the user and returns a session key, nonce tuple or boolean if false"""
    # print("in receive message")
    # print(message)
    if message is None:
        return False
    nonce_1 = message["nonce"]
    verified_auth = verify_auth(json.loads(message["auth"]))    # user_id, role, pub_key
    # print("verified auth")
    # print(verified_auth)
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
    # print()
    # print(ticket)
    # print()
    encrypted_ticket = fernet_ticket.encrypt(json.dumps(ticket).encode('latin1'))
    return encrypted_ticket


def create_message_1(nonce):
    """Takes in a nonce from client's original message and returns a json object
     with a signed nonce 1 and plaintext nonce 2"""
    signed_nonce_1 = server_private_key.sign(
        nonce.encode('latin1'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA256()
        )
    nonce_2 = os.urandom(16) # .decode('latin1')
    # print(signed_nonce_1.decode('latin1'))
    message = {
        "nonce_1": nonce,
        "signature": signed_nonce_1.decode('latin1'),
        "nonce_2": nonce_2.decode('latin1'),
    }
    return message


def receive_message_2(message, nonce_2):
    """Takes in the entire message containing the user signed nonce 2 and timestamp and returns a boolean if valid"""
    # fetch users public key from auth database
    match = 0  # valid
    # print(nonce_2.encode('latin1'))
    data_json = {
        "nonce": nonce_2,
        "timestamp": message["timestamp"]
    }
    # print(message["signature"].encode('latin1'))
    if not verify_timestamp(message["timestamp"]):
        return 1  # time out

    byte_json = json.dumps(data_json).encode('latin1')
    try:
        user_public_key.verify(
            message["signature"].encode('latin1'),
            byte_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
    except:
        # print("INVALID SIG")
        match = 2  # invalid signature
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


        data_in_1 = secure_sock.read(2048)
        print("RECEIVED MESSAGE 1:")
        print(data_in_1.decode('latin1'))
        bytes_in_1 = json.loads(data_in_1.decode('latin1'))
        message_in_1 = receive_message_1(bytes_in_1)  # user_id, role, pub_key, nonce_1
        if not message_in_1:
            # invalid auth
            message_out_1 = "Invalid Auth"
            bytes_out_1 = message_out_1.encode('latin1')
            secure_sock.write(bytes_out_1)
        else:
            # print("SUCCESSFUL AUTH")
            # print(message_in_1[2])
            #####################################
            user_public_key = serialization.load_pem_public_key(
                message_in_1[2],
                backend=default_backend()
            )
            # print("NEW KEY")
            # print(message_in_1[2])
            #####################################
            message_out_1 = create_message_1(message_in_1[3])
            print("MESSAGE OUT 1:")
            print(message_out_1)
            nonce_2 = message_out_1["nonce_2"]
            bytes_out_1 = json.dumps(message_out_1).encode('latin1')
            secure_sock.write(bytes_out_1)
            # receive message
            data_in_2 = secure_sock.read(2048)
            print("RECEIVED MESSAGE 2:")
            print(data_in_2.decode('latin1'))
            bytes_in_2 = json.loads(data_in_2.decode('latin1'))
            message_in_2 = receive_message_2(bytes_in_2, nonce_2)
            if message_in_2 == 1:
                # time expired
                message_out_2 = "Timed out"
                bytes_out_2 = message_out_2.encode('latin1')
                secure_sock.write(bytes_out_2)
            elif message_in_2 == 2:
                # bad signature
                message_out_2 = "Invalid response"
                bytes_out_2 = message_out_2.encode('latin1')
                secure_sock.write(bytes_out_2)
            else:
                # success
                message_out_2 = create_message_2(message_in_1[0], message_in_1[1])
                print("MESSAGE OUT 2:")
                print(message_out_2)
                secure_sock.write(message_out_2)

        # finally:
        secure_sock.close()
        server_socket.close()
