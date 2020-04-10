#Solomon Wang

import os
import os.path
import sys

patientID = "temp"
docID = 'temp'
timestamp = 'temp'
ticketts = 'temp'
#sessionKey = 'temp'                                        #key to decrypt the message AES{pID, Ticket, TS}
#^no longer needed, ssl should handle it

ticketKey = 'temp'                                         #key to decrypt the ticket
dataKey = b'\xad&dB\xfdLA4\xb9kjV\xc2\x0f\xab\x1e'          #key to decrypt the data from the record server\

record = 'temp'
aesRecord = 'temp'


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
			if record.doctor ID == docID:                     # if doctor ID matches docID from ticket; i.e., doctor is allowed access
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


def decryptTicket():
	#decrypt aes using ticketKey


def dataRequest(pID):                                      #open file folder and look for file with pID
	path = 'Database/Patient Records/'
	fileList = os.listdir(path)
	for i in fileList:
		if os.path.isfile(pID + '.pdf')
    		#return file back 
		else
			print('Patient file does not exist!')
			return -1
		








