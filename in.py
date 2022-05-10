import mysql.connector
import datetime
import ftplib
import cv2
import socket
import os
import sys
import threading
from tkinter import *
APP_STAT = True


def main_method():
    while(True) and APP_STAT == True:
        print("1")
        # pass


def app_stop():
    APP_STAT = False
    print("here")
    sys.exit()


t1 = threading.Thread(target=main_method)
t2 = threading.Thread(target=app_stop)


def thread1():

    t1.start()


def thread2():

    t2.start()


root = Tk()
root.title("in.py")
root.geometry('400x200')
Start_butt = Button(root, text="Start", command=thread1)
Stop_butt = Button(root, text="Stop", command=app_stop)
Start_butt.grid(row=0, column=0)
Stop_butt.grid(row=1, column=0)
root.mainloop()
