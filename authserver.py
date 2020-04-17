from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import json
import sqlite3
import textwrap
import os
import time

with sqlite3.connect("doctor_database.db") as db:
    cursor = db.cursor()

with open("authkey.txt", "rb") as fo:
    '''Key for encryption/decryption'''
    dataKey = fo.read()

auth_key = Fernet(dataKey)


TIMEOUT = 5  # minutes
doctor_public_key = None
doctor_private_key = None

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
    # will update with the proper hash function later
    hash_id = hash(user_id)
    hash_pw = hash(user_pw)

    find_user = "SELECT * FROM user WHERE user_id = ? AND user_pw = ?"
    cursor.execute(find_user, [hash_id, hash_pw])
    results = cursor.fetchall()

    # if auth matches, return the role and public key
    public_key = auth_key.decrypt(results[3])
    if results:
        return results[2], public_key
    else:
        return False


# def verify_signature(signature):
#     """Takes in a signed object and compares to values previously sent to client and returns a boolean"""


def receive_message_1(message):
    """Takes in the entire message after the initial key exchange from
    the user and returns a session key, nonce tuple or boolean if false"""
    json_plaintext = message
    nonce_1 = json_plaintext["nonce"]
    role, pub_key = verify_auth(json_plaintext["auth"])
    if pub_key:
        return role, pub_key, nonce_1
    else:
        return False


def create_ticket(doctor_id, role):
    """Takes in a doctor id and returns an encrypted json ticket"""
    ticket = {
        "doctor_id": doctor_id,
        "role": role,
        "timestamp": time.time()
    }
    # NEED TO MAKE SURE USER HAS AUTH SERVER PUBLIC KEY
    encrypted_ticket = fernet_ticket.encrypt(ticket)
    return encrypted_ticket


def create_message_1(nonce, timestamp):
    """Takes in a nonce from client's original message and returns a json object
     with a signed nonce 1 and plaintext nonce 2 and timestamp"""
    encrypted_nonce_1 = fernet_nonce.encrypt(nonce)
    nonce_2 = os.urandom(16)
    message = {
        "nonce_1": encrypted_nonce_1,
        "nonce_2": nonce_2,
        "timestamp": timestamp
    }
    return message


def receive_message_2(message):
    """Takes in the entire message containing the user signed nonce 2 and timestamp and returns a boolean if valid"""
    # fetch doctors public key from auth database
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
        doctor_public_key.verify(
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


def create_message_2(doctor_id):
    """Takes in a doctor id and role and combines with timestamp and returns an encrypted ticket"""
    # might change later if useless

    ticket = create_ticket(doctor_id, role)
    return ticket


bytes_in_1 = None
message_in_1= receive_message_1(bytes_in_1)  #role, pub_key, nonce_1
doctor_public_key = message_in_1[1]

if message_in_1 is None:
    #invalid auth
else:
    timestamp = time.time()
    message_out_1 = create_message_1(message_in_1[2])
    #bytes_out_1
    #send message
    #receive message
    bytes_in_2 = None
    message_in_2 = receive_message_2(bytes_in_2)
    if message_in_2 is None:
        #time expired
    elif message_in_2 == False:
        #bad signature
    else:
        message_out_2 = create_message_2()
        #bytes_out_2