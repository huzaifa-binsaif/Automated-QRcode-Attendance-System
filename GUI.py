import tkinter
from tkinter import *
import tkinter.messagebox
from PIL import Image,ImageTk
import time
import getpass
from tqdm.auto import tqdm
import pyzbar.pyzbar
import pyqrcode
import cv2
import os
import datetime
import mysql.connector
import numpy as np
from PIL import Image
from cryptography.fernet import Fernet
import tkinter

top = tkinter.Tk()
#................................................................................................................

key = b'2jwyEjZD6vCRBPn1Hf8YgyBWRBhtw9S53WefhwxCG6o='

def decrypt(en_text):
    fernet = Fernet(key)
    de_text = fernet.decrypt(en_text).decode()
    return de_text

def entry():
    win = Tk()

    win.geometry("700x700")
    win.title("SCINNOVA V Attendance Portal")
    #p3 = PhotoImage(file = "Scinnova 5 logo.png")
    #win.iconphoto(False,p3)
    global frame2
    frame2 = Frame(win, bg="#370006", height=700, width=700)
    frame2.pack(expand = True, fill = BOTH)
    label3 = Label(frame2, text = "Check Attendance", font=("helvetica", 30, "bold"), bg="#370006", fg="white")
    label3.pack(pady=(40,10))
    global e
    e = Entry(frame2, width = 70)
    e.pack(pady=60)
    btn4 = Button(frame2, bg="#3B638C", text="Enter",padx=10, pady=10, fg="white", command=view_person_attendance)
    btn4.pack(pady = (0,30))
    btn5 = Button(frame2, bg="#3B638C", text="Close window",padx=10, pady=10, fg="white", command=win.destroy)
    btn5.pack(side="bottom", padx=20, pady = (0,30))



def view_person_attendance():

    print(e.get())
    #Ask Owner(Huzaifa_binsaif) for access to original file 
    #Use MySql connector here
    #ie..
    #conn = mysql.connector.connect(
        #host="111.000.111.000",
        #user="Your Username",
        #password="XXXXXXXXXX,
        #database="Name of Database"
    #)
    c = conn.cursor()
    P_name = e.get()
    c.execute("SELECT name, teamid, status, TimeofMark FROM Attendance WHERE name = %s", (P_name,))
    rows = c.fetchall()
    for row in rows:
        listTostr = '  '.join([str(elem) for elem in row])
        label3 = Label(frame2, text = listTostr, font=("helvetica", 10, "bold"), bg="#370006", fg="white")
        label3.pack(pady=10)
        print(row)
    conn.close()




def scan():


    i = 0
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    while i < 1:
        _, frame = cap.read()
        decodeObject = pyzbar.pyzbar.decode(frame)
        for obj in decodeObject:
            name = obj.data
            name2 = decrypt(name)
            nn, ii, id, cc, mm = name2.split("  ")
            root = Toplevel()
            root.geometry("700x700")
            root.title("SCINNOVA V Attendance Portal")
            p2 = PhotoImage(file="Scinnova 5 logo.png ")
            root.iconphoto(False, p2)
            global my_image
            frame1 = Frame(root, bg="#370006", height=700, width=700)
            frame1.pack(expand = True, fill = BOTH)
            #C1 = tkinter.Canvas(root, bg="#370006", height=700, width=700)
            #C1.pack(expand=True, fill=BOTH)
            try:
                P_picture = Image.open("Participant Pictures/"+nn+".jpg")
            except:
                P_picture = Image.open("Participant Pictures/"+nn+".png")
            P_picture = P_picture.resize((255, 255), Image.ANTIALIAS)
            my_image = ImageTk.PhotoImage(P_picture)
            image_label2 = Label(frame1, image=my_image)
            image_label2.pack(pady=(30, 0))

            Name = Label(frame1, text="Name: {Participant_name}".format(Participant_name=nn), fg="white", font=("helvetica", 15, "bold"),bg="#370006")
            Name.pack(pady=(50, 0))

            Institution = Label(frame1, text="Institution: {Participant_team}".format(Participant_team=ii), fg="white", font=("helvetica", 15, "bold"), bg="#370006")
            Institution.pack(pady=(20, 0))


            Team = Label(frame1, text="Team: {Participant_team}".format(Participant_team=id), fg="white", font=("helvetica", 15, "bold"), bg="#370006")
            Team.pack(pady=(0, 20))

            Modules = Label(frame1, text="Modules: {Participant_modules}".format(Participant_modules=mm), fg="white", font=("helvetica", 15, "bold"), bg="#370006")
            Modules.pack(pady=(0,20))

            btn = Button(frame1, bg="#3B638C", text="Close window",padx=10, pady=10, fg="white", command=root.destroy)
            btn.pack(side="bottom", padx=20, pady=(0, 120))






            #userinput = input("Authenticate Participant and hit Enter otherwise hit CTRL+C")
                #Ask Owner(Huzaifa_binsaif) for access to original file 
                #Use MySql connector here
                #ie..
                #db = mysql.connector.connect(
                    #host="111.000.111.000",
                    #user="Your Username",
                    #password="XXXXXXXXXX,
                    #database="Name of Database"
            #)
            c = db.cursor()
            #c.execute("DROP TABLE IF EXISTS Attendance")
            c.execute("CREATE TABLE IF NOT EXISTS Attendance(name VARCHAR(255), institute VARCHAR(255), teamid VARCHAR(255), phone_no VARCHAR(255), modules VARCHAR(255), status VARCHAR(255), TimeofMark VARCHAR(255))")
            #c.execute("SELECT participant_status FROM Participant WHERE participant_name = {participant_name}".format(participant_name = nn))
            #ss = c.fetchone()
            #print(ss)
            ts = time.time()
            currentDateTime = str(datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
            print(currentDateTime)
            print(name2+" "+currentDateTime)
            c.execute("SELECT participant_status FROM Participant WHERE participant_name = %s", (nn,))
            stat = c.fetchall()
            listTostr = '  '.join([str(elem) for elem in stat])
            stat = listTostr.split("'")
            stat = stat[1].split("'")
            stat = str(stat[0])
            print(stat)
            if stat == "SIGNED OUT":
                ss = "SIGNED IN"
                #print(ss)
            elif stat == "SIGNED IN":
                ss = "SIGNED OUT"
            #print(ss)
            c.execute("UPDATE Participant set participant_status = %s WHERE participant_name = %s", (ss,nn,))
            c.execute("INSERT INTO Attendance(name, institute, teamid, phone_no, modules, status, TimeofMark) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                      (nn, ii, id, cc, mm, ss, currentDateTime))
            db.commit()
            i += 1

#Database portions
        cv2.imshow("QRcode", frame)
        if cv2.waitKey(1) & 0xff == ord("s"):
            break
            cv2.destroyAllWindows()
            cv2.release()

#...................................................................................................................
top.geometry("700x700")

top.title("SCINNOVA V Attendance Portal")
p1 = PhotoImage(file = "Scinnova 5 logo.png")
top.iconphoto(False,p1)

frame = Frame(top, bg="#370006", height=700, width=700)
frame.pack(expand = True, fill = BOTH)

C = tkinter.Canvas(frame, bg="#370006", height=700, width=700)
C.pack(expand=True, fill=BOTH)




Logo = Image.open("Scinnova 5 logo white (1).png")
image2 = Logo.resize((280, 330), Image.ANTIALIAS)
Logo = ImageTk.PhotoImage(image2)
image_label = Label(C, image=Logo, bg="#370006").pack(pady = (30,0))
#image = C.create_image(205, 180, anchor="nw", image=Logo)

title1 = Label(C, text="SCINNOVA V", font=("helvetica", 40, "bold"), bg="#370006", fg="white")
title = Label(C, text="Attendance Portal", font=("helvetica", 15, "bold"), bg="#370006", fg="white")

title1.pack(pady=(20,0))
title.pack()

B1 = tkinter.Button(C, bg="#3B638C", text="Mark Attendance", padx=23, pady=10, fg="white", command=scan)
B2 = tkinter.Button(C, bg="#3B638C", text="Check Attendance",padx=20, pady=10, fg="white", command=entry)

B2.pack(side="bottom", padx=20, pady = (20,70))
B1.pack(side = "bottom" )
#C.pack()




top.mainloop()
