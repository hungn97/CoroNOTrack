from cryptography.fernet import Fernet
import json
import sqlite3
import textwrap

def decrypt_message(message):
    """Takes in an AES encrypted message and returns a decrypted json object"""

def encrypt_message(message):
    """Takes in a plaintext message and returns an AES encrypted object"""

def verify_timestamp(timestamp):
    """Takes in a timestamp to check if message is still valid and returns a boolean"""

def verify_auth(auth):
    """Takes in a json containing user id and password and returns a boolean"""

def verify_signature(signature):
    """Takes in a signed object and compares to values previously sent to client and returns a boolean"""

def create_message_1(nonce):
    """Takes in a nonce from client's original message and returns a json object
     with a signed nonce 1 and plaintext nonce 2 and timestamp"""

def create_message_2(doctor_id):
    """Takes in a doctor id and combines with timestamp and returns an encrypted ticket"""