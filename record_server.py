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
import sqlite3
import base64
from pathlib import Path
from struct import pack


with open("ticketkey.txt","r") as ticket_key_file:                                 #read ticket key from file
    ticket_key = ticket_key_file.read().encode('latin1')
tick = Fernet(ticket_key)

with open("rskey.txt","r") as record_key_file:                                   #read record key from file
    record_key = record_key_file.read().encode('latin1')
enc = Fernet(record_key)

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
    try:
        data = json.loads(requested_data.decode('latin1'))        #convert from bytes to string, then load json into data
    except:
        return
    patientID = data['patient_id'].encode('latin1')
    timestamp = data['ts']
    doc_num = data['doc_number']
    print(patientID)
    print(timestamp)
    print(doc_num)

    ticket = tick.decrypt(data['ticket'].encode('latin1'))
    ticket = json.loads(ticket)

    role = ticket["role"]
    verified, role = verifyTicket(data['ticket'], timestamp, patientID)
    if verified:                      #if ticket is valid
        print("Ticket verified")
        returned_query = dataRequest(patientID, doc_num, role)
        print(returned_query)


    else:
        print("Ticket could not be verified")
        returned_query = b'-3'

    length = pack('>Q', len(returned_query))

    # sendall to make sure it blocks if there's back-pressure on the socket
    secure_sock.sendall(length)
    secure_sock.sendall(returned_query)

    ack = secure_sock.recv(1)
    # handle bad ack


def verifyTicket(Ticket, timestamp, patientID):  
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

    if float(timestamp)-ticketts > 60:                         #verify ticket is valid
        print('Timestamp mismatch')
        return False, -1

    print('Timestamp is within acceptable range')

    #print(type(patientID))

    return True, role
    

def dataUpload(json_file):
    with open(json_file, 'rb') as fo:
        data = json.loads(fo.read())
    format_in(data) 

def accessctrl(doc_num, role):
    if doc_num == '1':
        access = '10'
        check = list(access)
        if (role == int(check[0]) or role == int(check[1])):
            return access
        else:
            print('Sorry you are not allowed to access this file!')
            return -1

    elif doc_num == '2':
        access = '20'
        check = list(access)
        if (role == int(check[0]) or role == int(check[1])):
            return access
        else:
            print('Sorry you are not allowed to access this file!')
            return -1

    elif doc_num == '3':
        access = '12'
        check = list(access)
        if (role == int(check[0]) or role == int(check[1])):
            return access
        else:
            print('Sorry you are not allowed to access this file!')
            return -1
    
    elif doc_num == '4':
        access = '120'
        check = list(access)
        if (role == int(check[0]) or role == int(check[1]) or role == int(check[2])):
            return access
        else:
            print('Sorry you are not allowed to access this file!')
            return -1


def dataRequest(hpid, doc_num, role):
    
    access = accessctrl(doc_num,role)

    if access == -1:
        return b'-2'

    with sqlite3.connect("patient_database.db") as db:
        cursor = db.cursor()

    find_user = "SELECT * FROM user WHERE pid = ? AND role = ?"
    cursor.execute(find_user, [hpid,access])
    results = cursor.fetchone()
    # print("RESULTS")
    # print(results)
    if results:
        dec = enc.decrypt(results[3])
        # with open(os.path.join(
        #         '.', 'record2.pdf'), 'wb'
        # ) as fp:
        #     print(dec)
        #     fp.write(dec)
#         with open('result' + '.pdf', 'wb') as fo:
#             fo.write(base64.b64decode(dec))
        #########################################################################################################
        # type problem here, sending out a json when it should be bytes object
        r_record = {
            "record": dec.decode('latin1'),
            "signature": results[4].decode('latin1')
        }
        # print(r_record)
        return json.dumps(r_record).encode('latin1')
        ########################################################################################################
    else:
        print('\nError: Patient file does not exist!\n')
        return b'-1'
    
def format_out(name, record, ds): 
# Format to go out of record server

    data = {
        "record": record.decode("latin1"),
        "ds": ds.decode("latin1")
        }
    
    # with open(name +'.json', 'w') as fo:
    #     json.dump(data,fo)
    
    #return (name + '.json')
    return data

def format_in(data):
# Format to store into database
    with sqlite3.connect("patient_database.db") as db:
        cursor = db.cursor()

    aesdata = enc.encrypt(data['record'].encode('latin1'))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
        userid VARBINARY(300) NOT NULL,
        pid VARBINARY(300) NOT NULL,
        role VARBINARY(300) NOT NULL,
        aesdata VARBINARY(300) NOT NULL,
        ds VARBINARY(300) NOT NULL);
        """)
    ''' FORMAT : userid, H{pid}, role, AES{data}, ds'''

    params = (data['uid'],data['pid'].encode('latin1'),data['role'],aesdata,data['ds'].encode('latin1'))

    cursor.execute("""
        INSERT INTO user(userid, pid, role, aesdata, ds)
        VALUES(?,?,?,?,?)""", params)
    db.commit()

    cursor.execute("SELECT * FROM user")

# ############# Receive Message ###############
# data = message
# record = data["record"]
# ds = data["ds"])
# #############################################

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
sys.exit(0)


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
