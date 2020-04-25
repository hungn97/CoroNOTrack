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
import pickle
import time


with open("user_priv_key.pem", "rb") as key_file:
    user_private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

with open("auth_pub_key.pem", "rb") as key_file:
    auth_public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

def create_auth_message_1():
    """Takes in a user id and user pw and returns a plaintext json message"""
    user_id = input('Enter User ID\n>')
    user_pw = input('Enter User PW\n>')
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(user_pw.encode('latin1'))
    hashed_pw = pw_hash_func.finalize()
    auth = {
        "user_id": user_id,
        "user_pw": hashed_pw.decode('latin1')
    }
    nonce = os.urandom(16).decode('latin1')
    message = {
        "auth": json.dumps(auth),
        "nonce": nonce
    }
    #print(message)
    return message


def receive_auth_message_1(message):
    """Takes in the entire message containing the auth server signed nonce 1 and nonce 2
    and returns nonce 2 if valid"""
    # print(message["nonce_1"].encode('latin1'))
    match = message["nonce_2"].encode('latin1')
    try:
        auth_public_key.verify(
            message["signature"].encode('latin1'),
            message["nonce_1"].encode('latin1'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
    except:
        match = False
    return match


def create_auth_message_2(nonce_2):
    if nonce_2 is False:
        return "bad signature"
    timestamp = time.time()
    signature_data = {
        "nonce": nonce_2.decode('latin1'),
        "timestamp": timestamp
    }
    # print(json.dumps(signature_data))
    signature = user_private_key.sign(
        json.dumps(signature_data).encode('latin1'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA256()
        )
    message = {
        "signature": signature.decode('latin1'),
        "timestamp": timestamp
    }
    # print(signature)
    return message

def create_record_request(enc_ticket):
    req_pid = input('Enter Requested Patients ID\n>')
    timestamp = time.time()                         #get time for timestamp

    id_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())    #hash the patient id
    id_hash_func.update(req_pid.encode('latin1'))
    hashed_id = id_hash_func.finalize()

    request_data = {
        "patient_id":hashed_id.decode('latin1'),
        "ticket": enc_ticket.decode('latin1'),
        "ts": timestamp
    }

    message = json.dumps(request_data).encode('latin1')

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

    auth_message_out_1 = create_auth_message_1()                         #ask for user id and password
    auth_bytes_out_1 = json.dumps(auth_message_out_1).encode('latin')
    print("AUTH DATA OUT 1:")
    print(auth_bytes_out_1)
    secure_sock.write(auth_bytes_out_1)

    auth_data_in_1 = secure_sock.read(2048)
    print("AUTH DATA IN 1:")
    print(auth_data_in_1)
    auth_bytes_in_1 = json.loads(auth_data_in_1)
    nonce_2 = receive_auth_message_1(auth_bytes_in_1)
    auth_message_out_2 = create_auth_message_2(nonce_2)
    auth_bytes_out_2 = json.dumps(auth_message_out_2).encode('latin1')
    print("AUTH DATA OUT 2:")
    print(auth_bytes_out_2)
    secure_sock.write(auth_bytes_out_2)

    ticket = secure_sock.read(2048)
    print("AUTH DATA IN 2:")
    print(ticket)

    secure_sock.close() 
    sock.close()                              #close socket to auth server, open one to record server
    print("CONNECTION TO AUTH SERVER CLOSED")
    HOST = '127.0.0.1'
    PORT = 1235
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

    request = create_record_request(ticket);                    #create a record request using ticket from auth server
    secure_sock.write(request)

    requested_record = secure_sock.read(52000)
    print('--------------------------')
    print('Here is the requested record:')
    print(requested_record)

    #if verifyRecordSignature():

    #print('Requested record returned successfully')
    sys.exit(0)
