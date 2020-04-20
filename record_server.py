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

patientID = "temp"
docID = 'temp'
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

def getRecord(json_file):                          #pID is patient ID, Ticket is ticket from auth, TS is time stamp
    data = json.loads(fo.read())
    patientID = data['patient_id']
    timestamp = data['ts']

    if verifyTicket(data['ticket']):                      #if ticket is valid
        dataRequest(patientID)


def verifyTicket(Ticket):  
    ticket = tick.decrypt(Ticket.encode("latin1"))     
    docID = ticket['docID']
    ticketts = ticket['timestamp']
    role = ticket['role']

    patientFile = dataRequest(pID)                        #get requested patient data from files
    record = enc.decrypt(patientFile['record'].encode("latin1"))                           #decrypt patient file with dataKey
    #print(record)

    if (timestamp - ticketts) < 60:               #if time between ticket timestamp and when it was sent to record server < 1 min
        if record['role'] == role:
            if record['UID'] == docID:                     # if doctor ID matches docID from ticket; i.e., doctor is allowed access
                return true                             
            else:
                print('Doctor ID mismatch')
                return -1
        else:
            print('Incorrect role')
            return -1;
    else:
        print('time stamp is wrong')
        return -1
    

def dataUpload(json_file):
    path = 'Database/Patient Records/'
    fileList = os.listdir(path)

    for i in fileList:
        if os.path.isfile(os.path.join(path,json_file)):
            print('\nError: Patient file is already in the system!\n')
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

################################## UPLOAD ####################################
while True:
    #clear()
    choice = int(input("- Press '1' to UPLOAD a record.\n- Press '2' to RETRIEVE a record.\n- Press '3' to exit.\n"))

    if choice == 1:
        dataUpload(str(input("Enter name of file to upload: ")))
    elif choice == 2:
        dataRequest(str(input("Enter patientID: ")))
    elif choice == 3:
        exit()
    else:
        print("Please select a valid option!")
