import sqlite3
import aes

def main():
    with sqlite3.connect("doctor_database.db") as db:
        cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
            userid VARBINARY(300) NOT NULL,
            userpw VARBINARY(300) NOT NULL,
            patientid VARBINARY(300) NOT NULL,
            phone VARBINARY(300) NOT NULL,
            email VARBINARY(300) NOT NULL,
            first_name VARBINARY(300) NOT NULL,
            last_name VARBINARY(300) NOT NULL
    )""")

    User = aes.hash_password('30096073')
    Password = aes.hash_password('password')
    Phone = aes.encrypt('1111','(843)-254-5417')
    Email = aes.encrypt('1111','hunnguyen@umass.edu')
    FirstN = aes.encrypt('1111','Hung')
    LastN = aes.encrypt('1111','Nguyen')

    params = (User,Password,"1111",Phone,Email,FirstN,LastN)

    cursor.execute("""
    INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
    VALUES(?,?,?,?,?,?,?)""", params)

    User = aes.hash_password('12131415')
    Password = aes.hash_password('password')
    Phone = aes.encrypt('1112','(651)-433-6472')
    Email = aes.encrypt('1112','dylanbanh@umass.edu')
    FirstN = aes.encrypt('1112','Dylan')
    LastN = aes.encrypt('1112','Banh')

    params = (User,Password,"1112",Phone,Email,FirstN,LastN)

    cursor.execute("""
    INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
    VALUES(?,?,?,?,?,?,?)""", params)

    User = aes.hash_password('13141516')
    Password = aes.hash_password('password')
    Phone = aes.encrypt('1113','(144)-782-1916')
    Email = aes.encrypt('1113','lonnguyen@umass.edu')
    FirstN = aes.encrypt('1113','Long')
    LastN = aes.encrypt('1113','Nguyen')

    params = (User,Password,"1113",Phone,Email,FirstN,LastN)

    cursor.execute("""
    INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
    VALUES(?,?,?,?,?,?,?)""", params)

    User = aes.hash_password('14151617')
    Password = aes.hash_password('password')
    Phone = aes.encrypt('1114','(325)-755-9043')
    Email = aes.encrypt('1114','solomonwang@umass.edu')
    FirstN = aes.encrypt('1114','Solomon')
    LastN = aes.encrypt('1114','Wang')

    params = (User,Password,"1114",Phone,Email,FirstN,LastN)

    cursor.execute("""
    INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
    VALUES(?,?,?,?,?,?,?)""", params)

    db.commit()

    cursor.execute("SELECT * FROM user")
    print(cursor.fetchall())

def decrypting(patientid):
    if (patientid == '1111'):
        #User
        #Password
        Phone = aes.decrypt('1111',aes.encrypt('1111','(843)-254-5417')).decode('ascii')
        Email = aes.decrypt('1111',aes.encrypt('1111','hunnguyen@umass.edu')).decode('ascii')
        FirstN = aes.decrypt('1111',aes.encrypt('1111','Hung')).decode('ascii')
        LastN = aes.decrypt('1111',aes.encrypt('1111','Nguyen')).decode('ascii')
        
        return (Phone,Email,FirstN,LastN)

    if (patientid == '1112'):
        #User
        #Password
        Phone = aes.decrypt('1112',aes.encrypt('1112','(651)-433-6472')).decode('ascii')
        Email = aes.decrypt('1112',aes.encrypt('1112','dylanbanh@umass.edu')).decode('ascii')
        FirstN = aes.decrypt('1112',aes.encrypt('1112','Dylan')).decode('ascii')
        LastN = aes.decrypt('1112',aes.encrypt('1112','Banh')).decode('ascii')
        
        return (Phone,Email,FirstN,LastN)

    if (patientid == '1113'):
        #User
        #Password
        Phone = aes.decrypt('1113',aes.encrypt('1113','(144)-782-1916')).decode('ascii')
        Email = aes.decrypt('1113',aes.encrypt('1113','lonnguyen@umass.edu')).decode('ascii')
        FirstN = aes.decrypt('1113',aes.encrypt('1113','Long')).decode('ascii')
        LastN = aes.decrypt('1113',aes.encrypt('1113','Nguyen')).decode('ascii')
        
        return (Phone,Email,FirstN,LastN)

    if (patientid == '1114'):
        #User
        #Password
        Phone = aes.decrypt('1114',aes.encrypt('1114','(325)-755-9043')).decode('ascii')
        Email = aes.decrypt('1114',aes.encrypt('1114','solomonwang@umass.edu')).decode('ascii')
        FirstN = aes.decrypt('1114',aes.encrypt('1114','Solomon')).decode('ascii')
        LastN = aes.decrypt('1114',aes.encrypt('1114','Wang')).decode('ascii')
        
        return (Phone,Email,FirstN,LastN)

if __name__ == "__main__": 
    main()
else: 
    pass
