from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
import os.path
import sys
import json
import shutil
import hashlib
import binascii
import textwrap
import time
import socket
import ssl
import pprint
import pickle
from pathlib import Path

patientID = "temp"
userID = 'temp'
role = 5;
timestamp = 'temp'
ticketts = 'temp'
#sessionKey = 'temp'                                        #key to decrypt the message AES{pID, Ticket, TS}
#^no longer needed, ssl should handle it

ticketKey = 'Bwg2o7EMWUtYKYhtVq4eKQ-XBoA9ALKF4RAFjTDoZ5E='                                          #key to decrypt the ticket
dataKey = 'zDN1HN3taSHSHsvE0kAKRNY55VSTiLT9JEvjjXUfW2o='          #key to decrypt the data from the record server\

record = 'temp'
aesRecord = 'temp'

# Idea here is once the Json gets here, we look inside
# 
# If it has just the data and the ds,this means that the
# doctor is uploading the data into the database,
# -> Encrypt the data, pass the ds along and store the
#    encrypted data with the ds as one json file.
#
# If it has patientID, timestamp, ticket, this means that
# the doctor is retrieving a file, so we would have to 
# -> Verify the ticket making sure that it is still valid,
# -> If it is, we go into the record, decrypt the data 
#    and return the json that consists of the DECRYPTED 
#    data along with the ds.
#
# Main thing to keep note here is we don't touch the ds, just
# keep on passing it along with the encrypted/decrypted data

def getRecord(requested_data):                          #pID is patient ID, Ticket is ticket from auth, TS is time stamp
    data = json.loads(requested_data.decode('latin1'))        #convert from bytes to string, then load json into data
    patientID = data['patient_id']
    timestamp = data['ts']
    print(patientID)
    print(timestamp)

    if verifyTicket(data['ticket']):                      #if ticket is valid
        print("Ticket verified")
        #dataRequest(patientID)


def verifyTicket(Ticket):  
    ticket = tick.decrypt(Ticket.encode('latin1'))
    ticket = json.loads(ticket)
    #ticket = ticket.decode('latin1')

    userID = ticket["user_id"]
    ticketts = ticket["timestamp"]
    role = ticket["role"]

    print('Printing ticket information')
    print(userID)
    print(ticketts)
    print(role)

    if (timestamp - ticketts) < 60:
        print('Timestamp mismatch')
        return False

    print('Timestamp is within acceptable range')

    patientFile = dataRequest(patientID)                        #get requested patient data from files
    record = enc.decrypt(patientFile['record'].encode("latin1"))                           #decrypt patient file with dataKey

    if record['role'] == role:
        if record['did'] == userID:                     # if doctor ID matches docID from ticket; i.e., doctor is allowed access
            return True                             
        else:
                print('Doctor ID mismatch')
                return -1
    else:
        print('Incorrect role')
        return -1
    

def dataUpload(json_file):
    path = 'Database/Patient Records/'
    fileList = os.listdir(path)

    for i in fileList:
        if os.path.isfile(os.path.join(path,json_file)):
            ask = int(input('\nPatient file is already in the system! Would you like to update? 1 for Yes, 2 for No\n'))
            if ask == 1:
                os.remove(os.path.join(path,json_file))
                dataUpload(json_file)
            else:
                return -1
        else:
            with open(json_file) as fo:
                data = json.loads(fo.read())

                encrypted = enc.encrypt(data['record'].encode("latin1"))

                data['ds'] = data['ds'].encode("latin1")          
                # os.remove(json_file)
            shutil.move(format_in(json_file, encrypted, data['ds'], data['did'], data['pid'],data['role']), path)
            print('\nMessage: File successfully stored into the database!\n')
            break
                

def dataRequest(pID):                                      #open file folder and look for file with pID
    path = 'Database/Patient Records/'
    fileList = os.listdir(path)

    for i in fileList:
        if os.path.isfile(os.path.join(path,pID + '.json')):
            with open(os.path.join(path,pID + '.json')) as fo:

                data = json.loads(fo.read())
                dec = enc.decrypt(data['record'].encode("latin1"))
                print(data['ds'])
                
                with open(pID + '.pdf', 'wb') as fo:
                    fo.write(dec)
                data['ds'] = data['ds'].encode("latin1")

                format_out(pID,dec,data['ds'])
                
                print ('\nMessage: File successfully returned!\n')
                break
        else:
            print('\nError: Patient file does not exist!\n')
            return -1

def format_out(name, enc, ds): 
# Format to go out of record server
    data = {
        "record": enc.decode("latin1"),
        "ds": ds.decode("latin1") 
        }
    
    with open(name +'.json', 'w') as fo:
        json.dump(data,fo)
        
    return name + '.json'

def format_in(file_name, enc, ds, did, pid, role):
# Format to store into database
    
    data = {
        "did": did,
        "pid": pid,
        "role": role,
        "record": enc.decode('latin1'),
        "ds": ds.decode('latin1')
    }
    
    with open(file_name, 'w') as fo:
        json.dump(data,fo)
        
    return file_name

# ############# Receive Message ###############
# data = message
# record = data["record"]
# ds = data["ds"])
# #############################################

enc = Fernet(dataKey)
tick = Fernet(ticketKey)
clear = lambda: os.system('clear')

if __name__ == '__main__':
    print("record server starting")
    HOST = '127.0.0.1'
    PORT = 1235
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


        req_data = secure_sock.read(2048)
        print("RECEIVED REQUESTED DATA INFO:")
        getRecord(req_data)

        secure_sock.close()
        server_socket.close()
#sys.exit(0)


# ################################## UPLOAD ####################################
# while True:
#     #clear()
#     choice = int(input("- Press '1' to UPLOAD a record.\n- Press '2' to RETRIEVE a record.\n- Press '3' to exit.\n"))

#     if choice == 1:
#         dataUpload(str(input("Enter name of file to upload: ")))
#     elif choice == 2:
#         dataRequest(str(input("Enter patientID: ")))
#     elif choice == 3:
#         exit()
#     else:
#         print("Please select a valid option!")
