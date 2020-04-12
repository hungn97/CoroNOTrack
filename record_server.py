from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
import sys
import json
import shutil

patientID = "temp"
docID = 'temp'
timestamp = 'temp'
ticketts = 'temp'
#sessionKey = 'temp'                                        #key to decrypt the message AES{pID, Ticket, TS}
#^no longer needed, ssl should handle it

ticketKey = 'temp'                                          #key to decrypt the ticket
dataKey = b'\xad&dB\xfdLA4\xb9kjV\xc2\x0f\xab\x1e'          #key to decrypt the data from the record server\

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

def getRecord(pID, Ticket, TS):                          #pID is patient ID, Ticket is ticket from auth, TS is time stamp
		patientID = pID
		timestamp = TS

		if verifyTicket(Ticket, TS):                      #if ticket is valid

			aesRecord = aes.encrypt(record.data)               #encrypt record and signature
			return aesRecord                                   #send it back


def verifyTicket(Ticket, TS):       
	if decrypTicket():
		docID = ticket.docID
		ticketts = Ticket.timestamp

		patientFile = dataRequest(pID)                        #get requested patient data from files
		record = decrypt(patientFile)                           #decrypt patient file with dataKey

		if (timestamp - ticketts) < 1:               #if time between ticket timestamp and when it was sent to record server < 1 min
			if record.doctorID == docID:                     # if doctor ID matches docID from ticket; i.e., doctor is allowed access
				return true                             #ticket is verified
			else:
				print('Doctor ID mismatch')
				return -1
		else:
			print('time stamp is wrong')
			return -1

	else:
		print("Invalid ticket.")
		return -1                                #ticket cannot be decrypted, error

def dataUpload(json_file):
    path = 'Database/Patient Records/'
    fileList = os.listdir(path)
    file_name = json_file.split('.')
    name = file_name[0]

    for i in fileList:
        if os.path.isfile(os.path.join(path,json_file)):
            print('\nError: Patient file is already in the system!\n')
            return -1
        else:
            with open(json_file) as fo:
                data = json.loads(fo.read())
                encrypted = enc.encrypt(data['record'].encode("latin1"), dataKey)
                data['ds'] = data['ds'].encode("latin1")          
                os.remove(json_file)
            shutil.move(enc.format(name, encrypted, data['ds']), path)
            print('\nMessage: File successfully stored into the database!\n')
                

def dataRequest(pID):                                      #open file folder and look for file with pID
    path = 'Database/Patient Records/'
    fileList = os.listdir(path)
    for i in fileList:
        if os.path.isfile(os.path.join(path,pID + '.json')):
            with open(os.path.join(path,pID + '.json')) as fo:
                data = json.loads(fo.read())
                dec = enc.decrypt(data['record'].encode("latin1"), dataKey)
                with open(pID + '.pdf', 'wb') as fo:
                    fo.write(dec)
                data['ds'] = data['ds'].encode("latin1")
                enc.format(pID,dec,data['ds'])
                print ('\nMessage: File successfully returned!\n')
                break
        else:
            print('\nError: Patient file does not exist!\n')
            return -1

class Hung:

    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file): # A byte array will be coming in to be encrypted into a file
        name = str(input("Enter the patient ID of the patient you are uploading record for: "))
        with open(file, 'rb') as fo:
            plaintext = fo.read()                 # This will be coming in as data
        enc = self.encrypt(plaintext, self.key)     # Encrypt the data
        with open(name + ".pdf.enc", 'wb') as fo:   # Write it to a .enc file
            fo.write(enc) 
        # os.remove(plaintext)          
        self.format(name, enc, self.key)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, pid):
        with open(pid +'.json', 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(pid + '.pdf', 'wb') as fo:
            fo.write(dec)
        os.remove(pid + '.pdf.enc')

    def format(self, name, enc, ds): 
    # Format to store into database
        data = {
            "record": enc.decode("latin1"),
            "ds": ds.decode("latin1") 
        }
        with open(name +'.json', 'w') as fo:
            json.dump(data,fo)
        
        return name + '.json'

# ############# Receive Message ###############
# data = message
# record = data["record"]
# ds = data["ds"])
# #############################################

enc = Hung(dataKey)
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
