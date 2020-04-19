from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import sqlite3

with open("askey.txt", "rb") as fo:
    '''Key for encryption/decryption'''
    dataKey = fo.read()

enc = Fernet(dataKey)
#clear = lambda: os.system('clear')

with open("pub_key.pem", "rb") as key_file:
    '''This is the binary data of the key, this is only 
    for the sole purpose of AES{DPub}'''
    data = key_file.read().decode('utf-8')
    key = '\n'.join(data.split('\n')[1:-1]).encode('utf-8')

with open("pub_key.pem", "rb") as key_file:
    '''The public key to verify digital signature, we should
    still keep this to utilize the .verify function of the 
    cryptography library'''
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

def main():
    with sqlite3.connect("doctor_database.db") as db:
        cursor = db.cursor()

    # All the fields that will be include in the auth database
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
            userid VARBINARY(300) NOT NULL,    
            userpw VARBINARY(300) NOT NULL,
            role VARBINARY(300) NOT NULL,
            dpub VARBINARY(300) NOT NULL
    )""")
    ''' FORMAT : H{userid}, H{userpw}, role, AES{DPub}'''

    # DOCTOR #1: H{30096073}, H{password}, 1, AES{publickey}---------------------
    User = '30096073'
    Prehash_Password = 'password'
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(Prehash_Password.encode())
    Password = pw_hash_func.finalize()
    Role = '1'
    Dpub = enc.encrypt(key)

    params = (User, Password, Role, Dpub)

    cursor.execute("""
    INSERT INTO user(userid,userpw,role,dpub)
    VALUES(?,?,?,?)""", params)

    # PATIENT #1: H{12131415}, H{password}, 0, AES{publickey}---------------------
    User = '12131415'
    Prehash_Password = 'password'
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(Prehash_Password.encode())
    Password = pw_hash_func.finalize()
    Role = '0'
    Dpub = enc.encrypt(key)

    params = (User,Password,Role, Dpub)

    cursor.execute("""
    INSERT INTO user(userid,userpw,role,dpub)
    VALUES(?,?,?,?)""", params)

    # DOCTOR #2: H{13141516}, H{password}, 1, AES{publickey}---------------------
    User = '13141516'
    Prehash_Password = 'password'
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(Prehash_Password.encode())
    Password = pw_hash_func.finalize()
    Role = '1'
    Dpub = enc.encrypt(key)

    params = (User,Password,Role, Dpub)

    cursor.execute("""
    INSERT INTO user(userid,userpw,role,dpub)
    VALUES(?,?,?,?)""", params)

    # INSURANCE #1: H{14151617}, H{password}, 2, AES{publickey}---------------------
    User = '14151617'
    Prehash_Password = 'password'
    pw_hash_func = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pw_hash_func.update(Prehash_Password.encode())
    Password = pw_hash_func.finalize()
    Role = '2'
    Dpub = enc.encrypt(key)

    params = (User,Password,Role, Dpub)

    cursor.execute("""
    INSERT INTO user(userid,userpw,role, dpub)
    VALUES(?,?,?,?)""", params)

    db.commit()

    cursor.execute("SELECT * FROM user")
    print(cursor.fetchall())

if __name__ == "__main__": 
    main()
else: 
    pass
