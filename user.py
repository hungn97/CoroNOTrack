from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import socket
import ssl
from pathlib import Path
import json
import os
import time



def create_auth_message_1():
    """Takes in a user id and user pw and returns a plaintext json message"""
    user_id = input('Enter User ID\n>')
    user_pw = input('Enter User PW\n>')
    auth = {
        "user_id": user_id,
        "user_pw": user_pw
    }
    nonce = os.urandom(16).decode('latin1')
    message = {
        "auth": json.dumps(auth),
        "nonce": nonce
    }
    print(message)
    return message


# client
if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 1234
    cwd_path = Path.cwd()
    certs_path = str(cwd_path) + r"\sslsockets_commit"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1);
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(certs_path+r'\server.pem')
    context.load_cert_chain(certfile=certs_path+r"\client.pem", keyfile=certs_path+r"\client.key")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    cert = secure_sock.getpeercert()
    # print(cert)

    auth_message_out_1 = create_auth_message_1()
    auth_bytes_out_1 = json.dumps(auth_message_out_1).encode()
    print(auth_bytes_out_1)
    secure_sock.write(auth_bytes_out_1)
    print(secure_sock.read(1024))
    secure_sock.close()
    sock.close()