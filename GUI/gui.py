#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
import sqlite3
import aes
import patient_database
import doctor_database

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

    #------------------------- Initializing fonts for the rest of the GUIs -------------------------#
        self.helv28 = tkfont.Font(family='Helvetica', size=15)
        self.title_font = tkfont.Font(family='Helvetica', size=30, weight='bold', slant='italic')
        self.header_font = tkfont.Font(family='Helvetica', size=20, weight='bold')
        self.helv28b = tkfont.Font(family='Helvetica', size=15, weight='bold')
        self.helv28i = tkfont.Font(family='Helvetica', size=15, slant='italic')
    #-----------------------------------------------------------------------------------------------#


    #------------------------------ Initializing an array of Frames  -------------------------------#
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    #-----------------------------------------------------------------------------------------------#

    # GLOBAL VARIABLES:
        # Entries 1, 2 and 3 are used by the doctor
        self.entry1 = ''
        self.entry2 = ''
        self.entry3 = ''
        # Entries 4, 5, 6 and 7 are used by the patient
        self.entry4 = ''
        self.entry5 = ''
        self.entry6 = ''
        self.entry7 = ''        
        # The frames array
        self.frames = {}

    # START THE GUI, CREATE PAGE ONE. 
        self.new_frame(StartPage)

    def show_frame(self, page_name):
        # Show the frame of the given page_name
        frame = self.frames[page_name]
        frame.tkraise()

    def destroy_frame(self, page_name):
        # Destroy the frame of the given page_name
        frame = self.frames[page_name]
        frame.grid_remove()

    def new_frame(self, page_name):
        # Create the frame of the given page_name
        frame = page_name(parent=self.container, controller=self)
        self.frames[page_name.__name__] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(page_name.__name__)

    def restart_program(self):
        # Restarts the current program.
        # Note: this function does not return. Any cleanup action (like
        # saving data) must be done before calling this function.
        self.show_frame('StartPage')

        # Reset all the entries.
        if 'PageOne' in self.frames:
            self.entry1.delete(0,'end')
            self.entry2.delete(0,'end')
            self.entry3.delete(0,'end')
        if 'PageThree' in self.frames:
            self.entry4.delete(0,'end')
            self.entry5.delete(0,'end')
            self.entry6.delete(0,'end')
            self.entry7.delete(0,'end')

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #------------------------------ Title ------------------------------#
        label = tk.Label(self, text='CoroNO Track',
                         font=controller.title_font)
        #-------------------------------------------------------------------#
        label1 = tk.Label(self, text='You are a:',
                         font=controller.header_font)
        #-------------------------------------------------------------------#
        button1 = tk.Button(self, text='Doctor',
                            font=controller.helv28, command=lambda :
                            controller.new_frame(PageOne))
        #-------------------------------------------------------------------#
        button2 = tk.Button(self, text='Patient',
                            font=controller.helv28, command=lambda :
                            controller.new_frame(PageThree))
        #-------------------------------------------------------------------#
        # These following lines will put the above Widgets on the GUI
        label.pack(side='top', fill='x', pady=50)
        label1.place(relx=0.4, rely = 0.4)
        button1.place(relx=0.1, rely=0.5, relwidth=0.4, relheight=0.2)
        button2.place(relx=0.5, rely = 0.5, relwidth=0.4, relheight=0.2)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # CONNECT WITH THE DOCTOR DATABASE FILE THROUGH THE SQLITE3 CONNECTOR
        with sqlite3.connect("doctor_database.db") as db:
            self.cursor = db.cursor()
                
        #------------------------------ Title ------------------------------#
        label = tk.Label(self, text='Welcome',
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=20)
        #-------------------------------------------------------------------#
        label = tk.Label(self,text='Please Enter Your Information Below',font=controller.helv28i)
        label.pack(fill='x', pady=50)
        #-------------------------------------------------------------------#
        label1 = tk.Label(self,text='Badge ID')
        label1.pack()
        controller.entry1 = tk.Entry(self)
        controller.entry1.pack(pady=5)
        #-------------------------------------------------------------------#
        label2 = tk.Label(self,text='Password')
        label2.pack()
        controller.entry2 = tk.Entry(self,show='*')
        controller.entry2.pack(pady=5)
        #-------------------------------------------------------------------#
        label3 = tk.Label(self,text='Patient ID')
        label3.pack()
        controller.entry3 = tk.Entry(self)
        controller.entry3.pack(pady=5)
        #-------------------------------------------------------------------#
        button1 = tk.Button(self, text='Sign In', font=controller.helv28, command=lambda : self.next())
        button2 = tk.Button(self, text='Exit', font=controller.helv28, command=lambda : controller.restart_program())
        button1.place(relx=0.2, rely=0.65, relwidth=0.3, relheight=0.1)
        button2.place(relx=0.5, rely=0.65, relwidth=0.3, relheight=0.1)
        # The 'command' section is basically saying that this function will get perform once this button
        # is pressed, so in this case, if 'Sign In' was pressed, it will jump to the next() function

    def next(self):
        
        # GRAB INFOS FROM THE ENTRY FIELDS THAT THE DOCTOR HAS ENTERED FROM THE GUI
        doctorid = self.controller.entry1.get()
        doctorpw = self.controller.entry2.get()
        patientid = self.controller.entry3.get()

        #-------------------------------------------------------
        # Go through the whole database using a cursor, results will 
        # an array of all the results, which in our case there is only
        # one result, so result[0] is what we want.
        find_user = ("SELECT * FROM user WHERE patientid = ?")
        self.cursor.execute(find_user,[(patientid)])
        results = self.cursor.fetchall()
        #-------------------------------------------------------

        # IF FOUND:
        if results: 
            (Two,Three,Four,Five) = doctor_database.decrypting(patientid)
            # (Two,Three,Four,Five) = (Phone,Email,FirstN,LastN) from the doctor_database.
            if (aes.verify_password(results[0][0], doctorid)       # Verify the userid with the hashed userid in database.
                and aes.verify_password(results[0][1], doctorpw)): # Verify the password with the hashed password in database.
                for i in results:
                    self.controller.new_frame(PageTwo)
                    # If verified, show PageTwo which have all the informations requested aes_decrypted.
            else:
                query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
                query_label.place(relx=0.15, rely=0.60)

        # IF NOT FOUND:
        else:
            query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
            query_label.place(relx=0.15, rely=0.60)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # CONNECT WITH THE DATABASE FILES THROUGH THE SQLITE3 CONNECTOR
        with sqlite3.connect("doctor_database.db") as db:   # cursor for doctor_database
            self.cursor = db.cursor()
        with sqlite3.connect("patient_database.db") as db2: # cursor2 for patient_database
            self.cursor2 = db2.cursor()

        # GRAB INFOS FROM THE ENTRY FIELDS THAT THE DOCTOR HAS ENTERED FROM THE GUI
        doctorid = controller.entry1.get()
        doctorpw = controller.entry2.get()
        patientid = controller.entry3.get()
        id = patientid

        #-------------------------------------------------------
        # Go through the whole database using a cursor, results will 
        # an array of all the results, which in our case there is only
        # one result, so result[0] is what we want.
        find_user = ("SELECT * FROM user WHERE patientid = ?")
        self.cursor.execute(find_user,[(patientid)])
        results = self.cursor.fetchall()
        find_patient = ("SELECT * FROM patients WHERE id = ?")
        self.cursor2.execute(find_patient,[(id)])
        results2 = self.cursor2.fetchall()
        # We want to do the same with the patient_database, because
        # realistically the only thing that map up the two databases
        # is the patientid that we left open without performing any
        # kind of encryption on.
        result2 = results2[0]   #(Phone,Email,FirstN,LastN) from the doctor_database
        result = results[0]     #(FirstN,LastN,Address,City,State,Zip,Phone,Email,Ename,Ephone) from the patient_database
        #-------------------------------------------------------

        (Two,Three,Four,Five) = doctor_database.decrypting(patientid)
        #(Phone,Email,FirstN,LastN) from the doctor_database
        (Six,Seven,Eight,Nine,Ten,Eleven,Twelves,Thirteen,Fourteen,Fifteen) = patient_database.decrypting(patientid)
        #(FirstN,LastN,Address,City,State,Zip,Phone,Email,Ename,Ephone) from the patient_database

        #------------------------------------------------------ Header -------------------------------------------------------#
        label = tk.Label(self, text='Welcome, Dr. ' + Four + ' ' + Five , font=controller.header_font)
        label.pack(side='top', pady=20)
        query_label = tk.Label(self, text="Attached below is the patient's information that you requested.", font = controller.helv28i)
        query_label.place(relx=0.1, rely=0.1)
        #---------------------------------------------------------------------------------------------------------------------#

        # MATCH UP GAME, MATCH THESE INFOS WITH THE APPROPRIATE NUMBER
        # I realized how confusing it is, should've just use FirstN, LastN instead of One, Two, etc... sowwy
        line1 = tk.Label(self, text = "First Name: " + Six)
        line1.place(relx=0.15, rely=0.2)
        line2 = tk.Label(self, text = "Last Name: " + Seven)
        line2.place(relx=0.15, rely=0.25)
        line3 = tk.Label(self, text = "Address: " + Eight)
        line3.place(relx=0.15, rely=0.3)
        line4 = tk.Label(self, text = "City: " + Nine)
        line4.place(relx=0.15, rely=0.35)
        line5 = tk.Label(self, text = "State: " + Ten)
        line5.place(relx=0.15, rely=0.4)
        line6 = tk.Label(self, text = "Zipcode: " + Eleven)
        line6.place(relx=0.15, rely=0.45) 
        line7 = tk.Label(self, text = "Phone Number: " + Twelves)
        line7.place(relx=0.15, rely=0.5)
        line8 = tk.Label(self, text = "Email: " + Thirteen)
        line8.place(relx=0.15, rely=0.55)
        line9 = tk.Label(self, text = "Emergency Contact: " + Fourteen, font = controller.helv28i)
        line9.place(relx=0.15, rely=0.6)
        line10 = tk.Label(self, text = "Emergency Phone: " + Fifteen, font = controller.helv28i)
        line10.place(relx=0.15, rely=0.65)

        button1 = tk.Button(self, text="Exit",
                           command=lambda: controller.restart_program())
        button1.place(relx = 0.4, rely = 0.75, relwidth = 0.2, relheight = 0.1)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # CONNECT WITH THE PATIENT DATABASE FILE THROUGH THE SQLITE3 CONNECTOR
        with sqlite3.connect("patient_database.db") as db:
            self.cursor = db.cursor()

        #------------------------------ Title ------------------------------#
        label = tk.Label(self, text='Welcome',
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=20)
        #-------------------------------------------------------------------#
        label = tk.Label(self,text='Please Enter Your Information Below',font=controller.helv28i)
        label.pack(fill='x', pady=50)
        #-------------------------------------------------------------------#
        label4 = tk.Label(self,text='First Name')
        label4.pack()
        controller.entry4 = tk.Entry(self)
        controller.entry4.pack(pady=5)
        #-------------------------------------------------------------------#
        label5 = tk.Label(self,text='Last Name')
        label5.pack()
        controller.entry5 = tk.Entry(self)
        controller.entry5.pack(pady=5)
        #-------------------------------------------------------------------#
        label6 = tk.Label(self,text='Patient ID#')
        label6.pack()
        controller.entry6 = tk.Entry(self)
        controller.entry6.pack(pady=5)
        #-------------------------------------------------------------------#
        label7 = tk.Label(self,text='Password')
        label7.pack()
        controller.entry7 = tk.Entry(self, show='*')
        controller.entry7.pack(pady=5)       
        #-------------------------------------------------------------------#
        button1 = tk.Button(self, text='Sign In',font=controller.helv28, command=lambda : self.next())
        button2 = tk.Button(self, text='Exit',font=controller.helv28,command=lambda : controller.restart_program())
        button1.place(relx=0.2, rely=0.7, relwidth=0.3, relheight=0.1)
        button2.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1)
        # The 'command' section is basically saying that this function will get perform once this button
        # is pressed, so in this case, if 'Sign In' was pressed, it will jump to the next() function


    def next(self):
        # GRAB INFOS FROM THE ENTRY FIELDS THAT THE PATIENT HAS ENTERED FROM THE GUI
        first_name = self.controller.entry4.get()
        last_name = self.controller.entry5.get()
        id = self.controller.entry6.get()
        password = self.controller.entry7.get()

        #-------------------------------------------------------
        # Go through the whole database using a cursor, results will 
        # an array of all the results, which in our case there is only
        # one result, so result[0] is what we want.
        find_patient = ("SELECT * FROM patients WHERE id = ?")
        self.cursor.execute(find_patient,[(id)])
        results = self.cursor.fetchall()
        #-------------------------------------------------------

        # IF FOUND:
        if results: 
            (Six,Seven,Eight,Nine,Ten,Eleven,Twelves,Thirteen,Fourteen,Fifteen) = patient_database.decrypting(id)
            #(FirstN,LastN,Address,City,State,Zip,Phone,Email,Ename,Ephone) from the patient_database
            if (first_name == Six                                  # Verify if first_name is equal FirstN in database
                and last_name == Seven                             # Verify if last_name is equal LastN in database
                and aes.verify_password(results[0][7], password)): # Verify if the password is the same as the unhashed password
                for i in results:
                    self.controller.new_frame(PageFour)
                    # If verified, show PageFour which have all the informations requested aes_decrypted.
            else:
                query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
                query_label.place(relx=0.15, rely=0.66)

        # IF NOT FOUND:
        else:
            query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
            query_label.place(relx=0.15, rely=0.66)

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # CONNECT WITH THE DATABASE FILES THROUGH THE SQLITE3 CONNECTOR
        with sqlite3.connect("doctor_database.db") as db:
            self.cursor = db.cursor()
        with sqlite3.connect("patient_database.db") as db2:
            self.cursor2 = db2.cursor()

        # GRAB INFOS FROM THE ENTRY FIELDS THAT THE PATIENT HAS ENTERED FROM THE GUI
        first_name = controller.entry4.get()
        last_name = controller.entry5.get()
        id = controller.entry6.get()
        password = controller.entry7.get()
        patientid = id

        #-------------------------------------------------------
        # Go through the whole database using a cursor, results will 
        # an array of all the results, which in our case there is only
        # one result, so result[0] is what we want.
        find_patient = ("SELECT * FROM patients WHERE id = ?")
        self.cursor2.execute(find_patient,[(id)])
        results2 = self.cursor2.fetchall()

        find_user = ("SELECT * FROM user WHERE patientid = ?")
        self.cursor.execute(find_user,[(patientid)])
        results = self.cursor.fetchall()
        # We want to do the same with the patient_database, because
        # realistically the only thing that map up the two databases
        # is the patientid that we left open without performing any
        # kind of encryption on.
        result2 = results2[0]     #(FirstN,LastN,Address,City,State,Zip,Phone,Email,Ename,Ephone) from the patient_database
        result = results[0]       #(Phone,Email,FirstN,LastN) from the doctor_database
        #-------------------------------------------------------

        (Two,Three,Four,Five) = doctor_database.decrypting(id)
        #(Phone,Email,FirstN,LastN) from the doctor_database
        (Six,Seven,Eight,Nine,Ten,Eleven,Twelves,Thirteen,Fourteen,Fifteen) = patient_database.decrypting(id)
        #(FirstN,LastN,Address,City,State,Zip,Phone,Email,Ename,Ephone) from the patient_database

        #------------------------------------------------------ Header -------------------------------------------------------#
        label = tk.Label(self, text='Welcome, ' + Six, font=controller.header_font)
        label.pack(side='top', fill='x', pady=20)
        query_label = tk.Label(self, text="Attached below is the information that you requested.", font = controller.helv28i)
        query_label.place(relx=0.15, rely=0.1)
        #---------------------------------------------------------------------------------------------------------------------#

        # MATCH UP GAME, MATCH THESE INFOS WITH THE APPROPRIATE NUMBER
        # I realized how confusing it is, should've just use FirstN, LastN instead of One, Two, etc... sowwy
        line1 = tk.Label(self, text = "First Name: " + Six)
        line1.place(relx=0.15, rely=0.2)
        line2 = tk.Label(self, text = "Last Name: " + Seven)
        line2.place(relx=0.15, rely=0.25)
        line3 = tk.Label(self, text = "Address: " + Eight)
        line3.place(relx=0.15, rely=0.3)
        line4 = tk.Label(self, text = "City: " + Nine)
        line4.place(relx=0.15, rely=0.35)
        line5 = tk.Label(self, text = "State: " + Ten)
        line5.place(relx=0.15, rely=0.4)
        line6 = tk.Label(self, text = "Zipcode: " + Eleven)
        line6.place(relx=0.15, rely=0.45) 
        line7 = tk.Label(self, text = "Phone Number: " + Twelves)
        line7.place(relx=0.15, rely=0.5)
        line8 = tk.Label(self, text = "Doctor Responsible: Dr. " + Four + ' ' + Five)
        line8.place(relx=0.15, rely=0.55)
        line9 = tk.Label(self, text = "Doctor Phone Number: " + Two)
        line9.place(relx=0.15, rely=0.6)
        line10 = tk.Label(self, text = "Doctor Email: " + Three)
        line10.place(relx=0.15, rely=0.65)

        button1 = tk.Button(self, text="Exit", command=lambda: controller.restart_program())
        button1.place(relx = 0.4, rely = 0.75, relwidth = 0.2, relheight = 0.1)

def main():
    app = SampleApp()
    # SET SIZE OF GUI:
    app.geometry('500x700')
    app.mainloop()

if __name__ == '__main__':
    main()
