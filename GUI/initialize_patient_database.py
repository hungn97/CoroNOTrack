import sqlite3
import aes
# have to download pycrypto (easy_install pycrypto)

def main():
    with sqlite3.connect("patient_database.db") as db:
        cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
                first_name VARBINARY(150) NOT NULL,
                last_name VARBINARY(150) NOT NULL,
                address VARBINARY(150) NOT NULL,
                city VARBINARY(150) NOT NULL,
                state VARBINARY(150) NOT NULL,
                zipcode VARBINARY(150) NOT NULL,
                phone VARBINARY(150) NOT NULL,
                password VARBINARY(150) NOT NULL,
                confirm VARBINARY(150) NOT NULL,
                id VARBINARY(150) NOT NULL,
                email VARBINARY(150) NOT NULL,
                ename VARBINARY(150) NOT NULL,
                ephone VARBINARY(150) NOT NULL
    )""")

    Bob = aes.encrypt('1111','Bob')
    Smith = aes.encrypt('1111','Smith')
    Address = aes.encrypt('1111','134 Marcus St.')
    City = aes.encrypt('1111','Amherst')
    State = aes.encrypt('1111','MA')
    Zip = aes.encrypt('1111','01003')
    Phone = aes.encrypt('1111','(411)-355-4321')
    Password = aes.hash_password('123456')
    Email = aes.encrypt('1111','bobsmith@gmail.com')
    Ename = aes.encrypt('1111','Alice Smith')
    Ephone = aes.encrypt('1111','(411)-355-1352')

    params = (Bob,Smith,Address,City,State,Zip,Phone,Password,Password,"1111",Email,Ename,Ephone)

    cursor.execute("""
    INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", params)

    Justin = aes.encrypt('1112','Justin')
    Bieber = aes.encrypt('1112','Bieber')
    Address = aes.encrypt('1112','112 Marston St.')
    City = aes.encrypt('1112','Amherst')
    State = aes.encrypt('1112','MA')
    Zip = aes.encrypt('1112','01003')
    Phone = aes.encrypt('1112','(413)-222-1312')
    Password = aes.hash_password('oof123')
    Email = aes.encrypt('1112','justinbieber@gmail.com')
    Ename = aes.encrypt('1112','Drake')
    Ephone = aes.encrypt('1112','(413)-222-4673')

    params = (Justin,Bieber,Address,City,State,Zip,Phone,Password,Password,"1112",Email,Ename,Ephone)

    cursor.execute("""
    INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", params)

    Travis = aes.encrypt('1113','Travis')
    Scott = aes.encrypt('1113','Scott')
    Address = aes.encrypt('1113','630 Massachusetts Ave.')
    City = aes.encrypt('1113','Amherst')
    State = aes.encrypt('1113','MA')
    Zip = aes.encrypt('1113','01003')
    Phone = aes.encrypt('1113','(617)-243-1125')
    Password = aes.hash_password('123oof')
    Email = aes.encrypt('1113','travisscott@gmail.com')
    Ename = aes.encrypt('1113','Kendall Jenner')
    Ephone = aes.encrypt('1113','(617)-243-3347')

    params = (Travis,Scott,Address,City,State,Zip,Phone,Password,Password,"1113",Email,Ename,Ephone)

    cursor.execute("""
    INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", params)

    Miley = aes.encrypt('1114','Miley')
    Cyrus = aes.encrypt('1114','Cyrus')
    Address = aes.encrypt('1114','8 Montello St.')
    City = aes.encrypt('1114','Amherst')
    State = aes.encrypt('1114','MA')
    Zip = aes.encrypt('1114','01003')
    Phone = aes.encrypt('1114','(857)-142-9573')
    Password = aes.hash_password('777hi')
    Email = aes.encrypt('1114','mileycyrus@gmail.com')
    Ename = aes.encrypt('1114','Billy Cyrus')
    Ephone = aes.encrypt('1114','(857)-142-7501')

    params = (Miley,Cyrus,Address,City,State,Zip,Phone,Password,Password,"1114",Email,Ename,Ephone)

    cursor.execute("""
    INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", params)

    db.commit()

    cursor.execute("SELECT * FROM patients")
    print(cursor.fetchall())

def decrypting(patientid):

    if (patientid == '1111'):
        Bob = aes.decrypt('1111',aes.encrypt('1111','Bob')). decode('ascii')
        Smith = aes.decrypt('1111',aes.encrypt('1111','Smith')). decode('ascii')
        Address = aes.decrypt('1111',aes.encrypt('1111','134 Marcus St.')). decode('ascii')
        City = aes.decrypt('1111',aes.encrypt('1111','Amherst')). decode('ascii')
        State = aes.decrypt('1111',aes.encrypt('1111','MA')). decode('ascii')
        Zip = aes.decrypt('1111',aes.encrypt('1111','01003')). decode('ascii')
        Phone = aes.decrypt('1111',aes.encrypt('1111','(411)-355-4321')). decode('ascii')
        #Password
        Email = aes.decrypt('1111',aes.encrypt('1111','bobsmith@gmail.com')).decode('ascii')
        Ename = aes.decrypt('1111',aes.encrypt('1111','Alice Smith')).decode('ascii')
        Ephone = aes.decrypt('1111',aes.encrypt('1111','(411)-355-1352')).decode('ascii')

        return (Bob,Smith,Address,City,State,Zip,Phone,Email,Ename,Ephone)

    if (patientid == '1112'):
        Justin = aes.decrypt('1112',aes.encrypt('1112','Justin')).decode('ascii')
        Bieber = aes.decrypt('1112',aes.encrypt('1112','Bieber')).decode('ascii')
        Address = aes.decrypt('1112',aes.encrypt('1112','112 Marston St.')).decode('ascii')
        City = aes.decrypt('1112',aes.encrypt('1112','Amherst')).decode('ascii')
        State = aes.decrypt('1112',aes.encrypt('1112','MA')).decode('ascii')
        Zip = aes.decrypt('1112',aes.encrypt('1112','01003')).decode('ascii')
        Phone = aes.decrypt('1112',aes.encrypt('1112','(413)-222-1312')).decode('ascii')
        #Password
        Email = aes.decrypt('1112',aes.encrypt('1112','justinbieber@gmail.com')).decode('ascii')
        Ename = aes.decrypt('1112',aes.encrypt('1112','Drake')).decode('ascii')
        Ephone = aes.decrypt('1112',aes.encrypt('1112','(413)-222-4673')).decode('ascii')   

        return (Justin,Bieber,Address,City,State,Zip,Phone,Email,Ename,Ephone)

    if (patientid == '1113'):
        Travis = aes.decrypt('1113',aes.encrypt('1113','Travis')).decode('ascii')
        Scott = aes.decrypt('1113',aes.encrypt('1113','Scott')).decode('ascii')
        Address = aes.decrypt('1113',aes.encrypt('1113','630 Massachusetts Ave.')).decode('ascii')
        City = aes.decrypt('1113',aes.encrypt('1113','Amherst')).decode('ascii')
        State = aes.decrypt('1113',aes.encrypt('1113','MA')).decode('ascii')
        Zip = aes.decrypt('1113',aes.encrypt('1113','01003')).decode('ascii')
        Phone = aes.decrypt('1113',aes.encrypt('1113','(617)-243-1125')).decode('ascii')
        #Password
        Email = aes.decrypt('1113',aes.encrypt('1113','travisscott@gmail.com')).decode('ascii')
        Ename = aes.decrypt('1113',aes.encrypt('1113','Kendall Jenner')).decode('ascii')
        Ephone = aes.decrypt('1113',aes.encrypt('1113','(617)-243-3347')).decode('ascii')

        return (Travis,Scott,Address,City,State,Zip,Phone,Email,Ename,Ephone)

    if (patientid == '1114'):
        Miley = aes.decrypt('1114',aes.encrypt('1114','Miley')).decode('ascii')
        Cyrus = aes.decrypt('1114',aes.encrypt('1114','Cyrus')).decode('ascii')
        Address = aes.decrypt('1114',aes.encrypt('1114','8 Montello St.')).decode('ascii')
        City = aes.decrypt('1114',aes.encrypt('1114','Amherst')).decode('ascii')
        State = aes.decrypt('1114',aes.encrypt('1114','MA')).decode('ascii')
        Zip = aes.decrypt('1114',aes.encrypt('1114','01003')).decode('ascii')
        Phone = aes.decrypt('1114',aes.encrypt('1114','(857)-142-9573')).decode('ascii')
        #Password
        Email = aes.decrypt('1114',aes.encrypt('1114','mileycyrus@gmail.com')).decode('ascii')
        Ename = aes.decrypt('1114',aes.encrypt('1114','Billy Cyrus')).decode('ascii')
        Ephone = aes.decrypt('1114',aes.encrypt('1114','(857)-142-7501')).decode('ascii')

        return (Miley,Cyrus,Address,City,State,Zip,Phone,Email,Ename,Ephone)

if __name__ == "__main__": 
    main()
else: 
    pass
