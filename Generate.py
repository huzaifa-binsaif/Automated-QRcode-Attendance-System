import tkinter
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
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


key = b'2jwyEjZD6vCRBPn1Hf8YgyBWRBhtw9S53WefhwxCG6o='


def encrypt(text):
    fernet = Fernet(key)
    en_text = fernet.encrypt(text.encode())
    return en_text


def decrypt(en_text):
    fernet = Fernet(key)
    de_text = fernet.decrypt(en_text).decode()
    return de_text


def add_User():
    Li = []
    P_name = str(input("Please Enter Participant's Name\n"))
    P_teamid = str(input("Please Enter Participant's Team Id\n"))
    P_contac = input("Please enter Participant's contact No\n")
    P_modules = input("Please enter Participant's Modules\n")
    P_status = "SIGNED OUT"
    Li.extend((P_name, P_teamid, P_contac, P_modules))
# Using list compression to covnert list to str
    listTostr = '  '.join([str(elem) for elem in Li])
    #print (listTostr)
    #print(Back.YELLOW + "Please Verify the Information")
    print("Participant Name         = " + P_name)
    print("Participant Team ID         = " + P_teamid)
    print("Participant Contact         = " + P_contac)
    print("Participant Modules         = " + P_modules)
    P_picture = Image.open("Participant Pictures/"+P_name+".jpg")
    P_picture.show()
    input("Press Enter to continue or CTRL+C to Break Operation")
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
    c.execute("INSERT INTO Participant(participant_name, participant_teamid, participant_contact, participant_modules, participant_status) VALUES (%s,%s,%s,%s,%s)",
              (P_name, P_teamid, P_contac, P_modules, P_status))
    conn.commit()
    conn.close()
    listTostr = encrypt(listTostr)
    qr = pyqrcode.create(listTostr)
    if not os.path.exists('./QrCodes'):
        os.makedirs('./QrCodes')
    qr.png('./QrCodes/'+P_name+'.png', scale=8)


add_User()
