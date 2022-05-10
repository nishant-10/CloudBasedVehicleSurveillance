from tkinter import *
import cv2
import datetime
import time
import threading
import subprocess
from PIL import ImageTk, Image
import ftplib
import socket
import os
import mysql.connector
import createdir

createdir.check_folders()
root = Tk()
root.title("CloSurv [MH05EJ4657]")
root.iconbitmap("app_icon/cctv.ico")
root.geometry("600x700")
root.minsize(600, 700)
root.maxsize(600, 700)
imageFrame = Frame(root, width=600, height=500)
imageFrame.grid(row=0, column=0, columnspan=3)
# make 3 vars for 3 subtasks, we work on (1)(2)<-- ivcam (3)is laptop
cap1 = cv2.VideoCapture(3)
framerate1 = cap1.get(cv2.CAP_PROP_FPS)
framecount1 = 0
cap2 = cv2.VideoCapture(2)
framerate2 = cap2.get(cv2.CAP_PROP_FPS)
framecount2 = 0
cap3 = cv2.VideoCapture(1)
framerate3 = cap3.get(cv2.CAP_PROP_FPS)
framecount3 = 0
# ftpconnections
try:
    ind_ftp_sess = ftplib.FTP('ftp.nishantjoshi.tech',
                              'indoor@nishantjoshi.tech', 'ftpadmin')
except:
    pass
REMOTE_FTP_SERVER = "ftp.nishantjoshi.tech"
app_status = True
display1 = Label(imageFrame)
display1.grid(row=0, column=0, padx=0, pady=2)


def_prev = ImageTk.PhotoImage(Image.open("app_icon/defprev3.png"))
show_prev_value = IntVar()


def prev_method():

    global show_prev_butt, def_prev, prev1, cb_prev_opt1, cb_prev_opt2, cb_prev_opt3, prev_frame
    if show_prev_value.get() == 1:
        prev_frame.grid_forget()
        cb_prev_opt1.grid_forget()
        cb_prev_opt2.grid_forget()
        cb_prev_opt3.grid_forget()
    else:
        prev_frame = LabelFrame(
            root, text='Camera Preview', bd=1, relief=SOLID)
        prev_frame.grid(row=2, columnspan=3, sticky=W, padx=10)
        cb_prev_opt1 = Button(prev_frame, text="Indoor Surveillance",
                              command=lambda: which_prev(1), width=20)
        cb_prev_opt2 = Button(prev_frame, text="Driver Drowsiness",
                              command=lambda: which_prev(2), width=20)
        cb_prev_opt3 = Button(prev_frame, text="Outdoor Surveillance",
                              command=lambda: which_prev(3), width=20)
        cb_prev_opt1.grid(row=2, column=0, padx=21, pady=10, sticky=W)
        cb_prev_opt2.grid(row=2, column=1, padx=21, pady=10, sticky=W)
        cb_prev_opt3.grid(row=2, column=2, padx=21, pady=10, sticky=W)


def which_prev(opt):
    global cap, display1

    if opt == 1:
        cap = cv2.VideoCapture(3)
        while True:
            success, image = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow("Frame", image)
    elif opt == 2:
        cap = cv2.VideoCapture(3)
        while True:
            success, image = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow("Frame", image)
    else:
        cap = cv2.VideoCapture(3)
        while True:
            success, image = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow("Frame", image)


prev_frame = LabelFrame(root, text='Camera Preview',
                        bd=1, relief=SOLID)
prev_frame.grid(row=2, columnspan=3, sticky=W, padx=10)
cb_prev_opt1 = Button(prev_frame, text="Indoor Surveillance",
                      command=lambda: which_prev(1), width=20)
cb_prev_opt2 = Button(prev_frame, text="Driver Drowsiness",
                      command=lambda: which_prev(2), width=20)
cb_prev_opt3 = Button(prev_frame, text="Outdoor Surveillance",
                      command=lambda: which_prev(3), width=20)
cb_prev_opt1.grid(row=2, column=0, padx=21, pady=10, sticky=W)
cb_prev_opt2.grid(row=2, column=1, padx=21, pady=10, sticky=W)
cb_prev_opt3.grid(row=2, column=2, padx=21, pady=10, sticky=W)


show_prev_butt = Checkbutton(root, text="No Preview", command=prev_method, variable=show_prev_value, onvalue=1,
                             offvalue=0, padx=240)
show_prev_butt.grid(row=3, column=0, sticky=W)

start_frame = LabelFrame(root, text="Start Options", bd=1, relief=SOLID)
start_frame.grid(row=4, columnspan=3, sticky=W, padx=10)
start_opt1_val = IntVar()
start_opt2_val = IntVar()
start_opt3_val = IntVar()
cb_start_opt1 = Checkbutton(
    start_frame, text="Indoor surv. & Driver Drow.", variable=start_opt1_val)
cb_start_opt2 = Checkbutton(
    start_frame, text="Outdoor surv.", variable=start_opt2_val)


def check_all():
    global cb_start_opt1, cb_start_opt2
    if start_opt3_val.get() == 1:
        start_opt1_val.set(0)
        start_opt2_val.set(0)
        cb_start_opt1.config(state=DISABLED)
        cb_start_opt2.config(state=DISABLED)
    else:
        cb_start_opt1.config(state=ACTIVE)
        cb_start_opt2.config(state=ACTIVE)


cb_start_opt3 = Checkbutton(start_frame, text="All",
                            command=check_all, variable=start_opt3_val)
cb_start_opt1.grid(row=4, column=0, padx=10, pady=10, sticky=W)
cb_start_opt2.grid(row=4, column=1, padx=41, pady=10, sticky=W)
cb_start_opt3.grid(row=4, column=2, padx=80, pady=10, sticky=W)


def cloud_menu(opt):
    if opt == 1:
        subprocess.Popen(
            r'explorer /select,"C:\Users\91882\Desktop\closurv\offline"')
    if opt == 2:
        os.system('python sync.py')


menubar = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Sync', menu=file)
file.add_command(label='Explore Files', command=lambda: cloud_menu(1))
file.add_command(label='Sync Files', command=lambda: cloud_menu(2))
root.config(menu=menubar)


def one():
    os.system('python indoor.py')


def two():
    os.system('python driverdrow.py')


def three():
    os.system('python outdoor.py')


def start_app():
    global start_opt1_val, start_opt2_val, start_opt3_val
    v1 = start_opt1_val.get()
    v2 = start_opt2_val.get()
    v3 = start_opt3_val.get()
    if v1 == 1:
        t1 = threading.Thread(target=one)
        t2 = threading.Thread(target=two)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
    if v2 == 1:
        t3 = threading.Thread(target=three)
        t3.daemon = True
        t3.start()
    if v3 == 1:
        t1 = threading.Thread(target=one)
        t2 = threading.Thread(target=two)
        t3 = threading.Thread(target=three)
        t3.daemon = True
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        t3.start()


start_butt = Button(start_frame, text="Start", width=25, command=start_app)
start_butt.grid(row=5, column=1, sticky=W, pady=10)


def on_closing():
    cap1.release()
    cap2.release()
    cap3.release()
    root.destroy()


# root.protocol("WM_DELETE_WINDOW", on_closing)
stop_butt = Button(start_frame, text="Stop", width=25, command=on_closing)
stop_butt.grid(row=6, column=1, sticky=W, pady=10)

root.mainloop()
