import sqlite3

with sqlite3.connect("patient_database.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL,
            address VARCHAR(20) NOT NULL,
            city VARCHAR(20) NOT NULL,
            state VARCHAR(20) NOT NULL,
            zipcode VARCHAR(20) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL,
            confirm VARCHAR(20) NOT NULL,
            id VARCHAR(20) NOT NULL,
            email VARCHAR(20) NOT NULL,
            ename VARCHAR(20) NOT NULL,
            ephone VARCHAR(20) NOT NULL
)""")

cursor.execute("""
INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
VALUES("Bob","Smith","134 Marcus St.", "Amherst", "MA", "01003", "(411)-355-4321", "123456", "123456", "1", "bobsmith@gmail.com", "Alice Smith", "(411)-355-1352")
""")

cursor.execute("""
INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
VALUES("Justin","Bieber","112 Marston St.", "Amherst", "MA", "01003", "(413)-222-1312", "oof123", "oof123", "2", "justinbieber@gmail.com", "Drake", "(413)-222-4673")
""")

cursor.execute("""
INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
VALUES("Travis","Scott","134 Marcus St.", "Amherst", "MA", "01003", "(617)-243-1125", "123oof", "123off", "3", "travisscott@gmail.com", "Kendall Jenner", "(617)-243-3347")
""")

cursor.execute("""
INSERT INTO patients(first_name,last_name,address,city,state,zipcode,phone,password,confirm,id,email,ename,ephone)
VALUES("Miley","Cyrus","134 Marcus St.", "Amherst", "MA", "01003", "(857)-142-9573", "777hi", "777hi", "4", "mileycyrus@gmail.com", "Billy Cyrus", "(857)-142-7501")
""")

db.commit()

cursor.execute("SELECT * FROM patients")
print(cursor.fetchall())

