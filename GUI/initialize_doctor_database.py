import sqlite3

with sqlite3.connect("doctor_database.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        userid INTEGER PRIMARY KEY,
        userpw VARCHAR(20) NOT NULL,
        patientid VARCHAR(20) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(20) NOT NULL,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20) NOT NULL
)""")

cursor.execute("""
INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
VALUES("30096073","password","1","(843)-254-5417","hunnguyen@umass.edu","Hung","Nguyen")
""")

cursor.execute("""
INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
VALUES("12131415","password","2","(651)-433-6472","dylanbanh@umass.edu","Dylan","Banh")
""")

cursor.execute("""
INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
VALUES("13141516","password","3","(144)-782-1916","lonnguyen@umass.edu","Long","Nguyen")
""")

cursor.execute("""
INSERT INTO user(userid,userpw,patientid,phone,email,first_name,last_name)
VALUES("14151617","password","4","(325)-755-9043","solomonwang@umass.edu","Solomon","Wang")
""")
db.commit()

cursor.execute("SELECT * FROM user")
print(cursor.fetchall())

