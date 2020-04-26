from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
import os.path
import sys
import json
import binascii
import hashlib
import base64

with open("priv_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

#digital signature
def create_signature(message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Read the pdf file, return a byte array 
def read_file(file_name,uid,pid,role):

    with open(file_name, 'rb') as fo:
        content= binascii.hexlify(fo.read())
######## MAKE KEY #########
    ds = create_signature(content)


    
    format_json(file_name,ds,uid,pid,role)

#verify digital signature
# def verify_signature(pub_key, message, ds):
#     h = SHA256.new(message)
#     rsa = RSA.importKey(pub_key)
#     signer = PKCS1_PSS.new(rsa)

#     result = "Message: Document Authenticity Verified" if (signer.verify(h, ds)) else "Warning: Document Authenticity Not Verified"
#     return result

# Read the pdf file, return a byte array 
def read_file(file_name,uid,pid,role):

    with open(file_name, 'rb') as fo:
        content= binascii.hexlify(fo.read())
######## MAKE KEY #########

    ds = create_signature(content)
    format_json(file_name,ds,uid,pid,role)

######### VERIFY ##########
    # with open('pub_key.txt', 'rb') as fp2:
    #     pub_key = fp2.read()

    # result = verify_signature(pub_key, content, ds)

# Format the bytes array + the ds
def format_json(file_name, ds, uid, pid, role):
# Format to store into database
    with open(file_name, 'rb') as fo:
        content= base64.b64encode(fo.read())

    pid_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pid_hash_func.update(pid.encode('utf-8'))
    hashed_pid = pid_hash_func.finalize()

    data = {
        "uid": uid,
        "pid": hashed_pid.decode('latin1'),
        "role": role,
        "record": content.decode('latin1'),
        "ds": ds.decode('latin1')
    }

    file_name = file_name.split('.')
    
    os.remove(file_name[0] + '.' + file_name[1])

    with open(file_name[0] +'_1.json', 'w') as fo:
        data['role'] = 10
        # Patient - Doctor
        json.dump(data,fo)
        print(data['pid'].encode('latin1'))

    with open(file_name[0] +'_2.json', 'w') as fp:
        data['role'] = 20
        # Patient - Insurance
        json.dump(data,fp)

    with open(file_name[0] +'_3.json', 'w') as fp:
        data['role'] = 12
        # Doctor - Insurance
        json.dump(data,fp)             

    with open(file_name[0] +'_4.json', 'w') as fp:
        data['role'] = 120
        # All Three
        json.dump(data,fp)                          

def getAllFiles():     
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirs = []
    for dirName, subdirList, fileList in os.walk(dir_path):
        for fname in fileList:
            if (fname != 'authdatabase.py' and fname != 'authkey.txt' 
               and fname != 'convertfiles.py'
               and fname != 'priv_key.pem' and fname != 'pub_key.pem'
               and fname != 'record_server.py' and fname != 'recordkey.txt'
               and fname != 'uploadfiles.py' and fname != '.DS_Store'
               and fname != 'duplicate.py'):
                dirs.append(dirName + "/" + fname)
    return dirs

def convert_one_file(file_name):
    uid = (str(input("Enter your ID: ")))
    pid = file_name.split('.')
    read_file(file_name,uid,pid[0],0)

def convert_all_files():
    dirs = getAllFiles()
    uid = (str(input("Enter your ID: ")))
    for file_name in dirs:
        realfile = file_name.split('/')
        pid = realfile[5].split('.')
        read_file(realfile[5],uid,pid[0],0)


while True:
    choice = int(input("1. Press '1' to convert 1 file.\n2. Press '2' to convert all files.\n3. Press '3' to exit.\n"))
    if choice == 1:
        convert_one_file (str(input("Enter your file to convert: ")))
    elif choice == 2:
        convert_all_files()
    elif choice == 3:
        exit()
    else:
        print("Please select a valid option!")