#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import sqlite3

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.helv28 = tkfont.Font(family='Helvetica', size=15)
        self.title_font = tkfont.Font(family='Helvetica', size=30, weight='bold', slant='italic')
        self.header_font = tkfont.Font(family='Helvetica', size=20, weight='bold')
        self.helv28b = tkfont.Font(family='Helvetica', size=15, weight='bold')
        self.helv28i = tkfont.Font(family='Helvetica', size=15, slant='italic')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Tkinter string variable # able to store any string value

        self.entry1 = ''
        self.entry2 = ''
        self.entry3 = ''
        self.entry4 = ''
        self.entry5 = ''
        self.entry6 = ''
        self.entry7 = ''        
        
        self.frames = {}
        self.new_frame(StartPage)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def destroy_frame(self, page_name):
        frame = self.frames[page_name]
        frame.grid_remove()

    def new_frame(self, page_name):
        frame = page_name(parent=self.container, controller=self)
        self.frames[page_name.__name__] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.

        frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(page_name.__name__)

    def restart_program(self):

        # Restarts the current program.
        # Note: this function does not return. Any cleanup action (like
        # saving data) must be done before calling this function."""

        # making sure all the entry are cleared and disable

        self.show_frame('StartPage')
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

        label = tk.Label(self, text='CoroNO Track',
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=50)

        label1 = tk.Label(self, text='You are a:',
                         font=controller.header_font)
        label1.place(relx=0.4, rely = 0.4)

        button1 = tk.Button(self, text='Doctor',
                            font=controller.helv28, command=lambda :
                            controller.new_frame(PageOne))

        button2 = tk.Button(self, text='Patient',
                            font=controller.helv28, command=lambda :
                            controller.new_frame(PageThree))

        button1.place(relx=0.1, rely=0.5, relwidth=0.4, relheight=0.2)
        button2.place(relx=0.5, rely = 0.5, relwidth=0.4, relheight=0.2)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        with sqlite3.connect("doctor_database.db") as db:
            self.cursor = db.cursor()

        label = tk.Label(self, text='Welcome',
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=20)

        label = tk.Label(self,text='Please Enter Your Information Below',font=controller.helv28i)
        label.pack(fill='x', pady=50)

        label1 = tk.Label(self,text='Badge ID')
        label1.pack()
        controller.entry1 = tk.Entry(self,text='Badge ID')
        controller.entry1.pack(pady=5)

        label2 = tk.Label(self,text='Password')
        label2.pack()
        controller.entry2 = tk.Entry(self,text='Password')
        controller.entry2.pack(pady=5)

        label3 = tk.Label(self,text='Patient ID')
        label3.pack()
        controller.entry3 = tk.Entry(self,text='Patient ID')
        controller.entry3.pack(pady=5)

        button1 = tk.Button(self, text='Sign In',
                            font=controller.helv28, command=lambda : \
                            self.next())
        button2 = tk.Button(self, text='Exit', font=controller.helv28,
                            command=lambda : controller.restart_program())
        button1.place(relx=0.2, rely=0.65, relwidth=0.3, relheight=0.1)
        button2.place(relx=0.5, rely=0.65, relwidth=0.3, relheight=0.1)

    def next(self):
        doctorid = self.controller.entry1.get()
        doctorpw = self.controller.entry2.get()
        patientid = self.controller.entry3.get()
        find_user = ("SELECT * FROM user WHERE userid = ? AND userpw = ? AND patientid = ?")
        self.cursor.execute(find_user,[(doctorid),(doctorpw),(patientid)])
        results = self.cursor.fetchall()

        if results:
            for i in results:
                self.controller.new_frame(PageTwo)

        else:
            query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
            query_label.place(relx=0.15, rely=0.60)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        with sqlite3.connect("doctor_database.db") as db:
            self.cursor = db.cursor()

        with sqlite3.connect("patient_database.db") as db2:
            self.cursor2 = db2.cursor()

        doctorid = controller.entry1.get()
        doctorpw = controller.entry2.get()
        patientid = controller.entry3.get()
        id = patientid

        find_user = ("SELECT * FROM user WHERE userid = ? AND userpw = ? AND patientid = ?")
        self.cursor.execute(find_user,[(doctorid),(doctorpw),(patientid)])
        results = self.cursor.fetchall()

        find_patient = ("SELECT * FROM patients WHERE id = ?")
        self.cursor2.execute(find_patient,[(id)])
        results2 = self.cursor2.fetchall()
    
        result2 = results2[0]
        result = results[0]

        label = tk.Label(self, text='Welcome, Dr. ' + str(result[5]) + ' ' + str(result[6]) , font=controller.header_font)
        label.pack(side='top', pady=20)

        query_label = tk.Label(self, text="Attached below is the patient's information that you requested.", font = controller.helv28i)
        query_label.place(relx=0.1, rely=0.1)

        line1 = tk.Label(self, text = "First Name: " + str(result2[0]))
        line1.place(relx=0.15, rely=0.2)
        line2 = tk.Label(self, text = "Last Name: " + str(result2[1]))
        line2.place(relx=0.15, rely=0.25)
        line3 = tk.Label(self, text = "Address: " + str(result2[2]))
        line3.place(relx=0.15, rely=0.3)
        line4 = tk.Label(self, text = "City: " + str(result2[3]))
        line4.place(relx=0.15, rely=0.35)
        line5 = tk.Label(self, text = "State: " + str(result2[4]))
        line5.place(relx=0.15, rely=0.4)
        line6 = tk.Label(self, text = "Zipcode: " + str(result2[5]))
        line6.place(relx=0.15, rely=0.45) 
        line7 = tk.Label(self, text = "Phone Number: " + str(result2[6]))
        line7.place(relx=0.15, rely=0.5)
        line8 = tk.Label(self, text = "Email: " + str(result2[10]))
        line8.place(relx=0.15, rely=0.55)
        line9 = tk.Label(self, text = "Emergency Contact: " + str(result2[11]), font = controller.helv28i)
        line9.place(relx=0.15, rely=0.6)
        line10 = tk.Label(self, text = "Emergency Phone: " + str(result2[12]), font = controller.helv28i)
        line10.place(relx=0.15, rely=0.65)

        button1 = tk.Button(self, text="Exit",
                           command=lambda: controller.restart_program())

        button1.place(relx = 0.4, rely = 0.75, relwidth = 0.2, relheight = 0.1)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        with sqlite3.connect("patient_database.db") as db:
            self.cursor = db.cursor()

        label = tk.Label(self, text='Welcome',
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=20)

        label = tk.Label(self,text='Please Enter Your Information Below',font=controller.helv28i)
        label.pack(fill='x', pady=50)

        label4 = tk.Label(self,text='First Name')
        label4.pack()
        controller.entry4 = tk.Entry(self)
        controller.entry4.pack(pady=5)

        label5 = tk.Label(self,text='Last Name')
        label5.pack()
        controller.entry5 = tk.Entry(self)
        controller.entry5.pack(pady=5)

        label6 = tk.Label(self,text='Patient ID#')
        label6.pack()
        controller.entry6 = tk.Entry(self)
        controller.entry6.pack(pady=5)

        label7 = tk.Label(self,text='Password')
        label7.pack()
        controller.entry7 = tk.Entry(self)
        controller.entry7.pack(pady=5)       

        button1 = tk.Button(self, text='Sign In',
                            font=controller.helv28, command=lambda : self.next())
        button2 = tk.Button(self, text='Exit', font=controller.helv28,
                            command=lambda : controller.restart_program())
        button1.place(relx=0.2, rely=0.7, relwidth=0.3, relheight=0.1)
        button2.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1)

    def next(self):
        first_name = self.controller.entry4.get()
        last_name = self.controller.entry5.get()
        id = self.controller.entry6.get()
        password = self.controller.entry7.get()

        find_patient = ("SELECT * FROM patients WHERE first_name = ? AND last_name = ? AND id = ? AND password = ?")
        self.cursor.execute(find_patient,[(first_name),(last_name),(id),(password)])
        results = self.cursor.fetchall()

        if results:
            for i in results:
                self.controller.new_frame(PageFour)

        else:
            query_label = tk.Label(self, text="We are not able to verify your information. Please try again.")
            query_label.place(relx=0.15, rely=0.66)

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        with sqlite3.connect("doctor_database.db") as db:
            self.cursor = db.cursor()

        with sqlite3.connect("patient_database.db") as db2:
            self.cursor2 = db2.cursor()

        first_name = controller.entry4.get()
        last_name = controller.entry5.get()
        id = controller.entry6.get()
        password = controller.entry7.get()
        patientid = id

        label = tk.Label(self, text='Welcome, ' + first_name, font=controller.header_font)
        label.pack(side='top', fill='x', pady=20)

        find_patient = ("SELECT * FROM patients WHERE first_name = ? AND last_name = ? AND id = ? AND password = ?")
        self.cursor2.execute(find_patient,[(first_name),(last_name),(id),(password)])
        results2 = self.cursor2.fetchall()

        find_user = ("SELECT * FROM user WHERE patientid = ?")
        self.cursor.execute(find_user,[(patientid)])
        results = self.cursor.fetchall()
    
        result2 = results2[0]
        result = results[0]

        query_label = tk.Label(self, text="Attached below is the information that you requested.", font = controller.helv28i)
        query_label.place(relx=0.15, rely=0.1)

        line1 = tk.Label(self, text = "First Name: " + str(result2[0]))
        line1.place(relx=0.15, rely=0.2)
        line2 = tk.Label(self, text = "Last Name: " + str(result2[1]))
        line2.place(relx=0.15, rely=0.25)
        line3 = tk.Label(self, text = "Address: " + str(result2[2]))
        line3.place(relx=0.15, rely=0.3)
        line4 = tk.Label(self, text = "City: " + str(result2[3]))
        line4.place(relx=0.15, rely=0.35)
        line5 = tk.Label(self, text = "State: " + str(result2[4]))
        line5.place(relx=0.15, rely=0.4)
        line6 = tk.Label(self, text = "Zipcode: " + str(result2[5]))
        line6.place(relx=0.15, rely=0.45) 
        line7 = tk.Label(self, text = "Phone Number: " + str(result2[6]))
        line7.place(relx=0.15, rely=0.5)
        line8 = tk.Label(self, text = "Doctor Responsible: Dr. " + str(result[5]) + ' ' + str(result[6]))
        line8.place(relx=0.15, rely=0.55)
        line9 = tk.Label(self, text = "Doctor Phone Number: " + str(result[3]))
        line9.place(relx=0.15, rely=0.6)
        line10 = tk.Label(self, text = "Doctor Email: " + str(result[4]))
        line10.place(relx=0.15, rely=0.65)


        button1 = tk.Button(self, text="Exit",
                           command=lambda: controller.restart_program())

        button1.place(relx = 0.4, rely = 0.75, relwidth = 0.2, relheight = 0.1)

def main():
    app = SampleApp()
    app.geometry('500x700')
    app.mainloop()

if __name__ == '__main__':
    main()
