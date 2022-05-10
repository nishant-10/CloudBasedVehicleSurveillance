from tkinter import *
import cv2
import datetime
import time
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
    ind_ftp_sess = ftplib.FTP('ftp.dummy',
                              'indoor@dummy', 'ftpdummy')
except:
    pass
REMOTE_FTP_SERVER = "ftp.dummy"
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
        cap = cv2.VideoCapture(2)
        while True:
            success, image = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow("Frame", image)
    else:
        cap = cv2.VideoCapture(1)
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
cb_start_opt1 = Checkbutton(start_frame, text="Indoor surv. & Driver Drow.")
cb_start_opt2 = Checkbutton(start_frame, text="Outdoor surv.")
cb_start_opt3 = Checkbutton(start_frame, text="All")
cb_start_opt1.grid(row=4, column=0, padx=10, pady=10, sticky=W)
cb_start_opt2.grid(row=4, column=1, padx=41, pady=10, sticky=W)
cb_start_opt3.grid(row=4, column=2, padx=80, pady=10, sticky=W)


def cloud_menu(opt):
    if opt == 1:
        subprocess.Popen(
            r'explorer /select,"C:\Users\91882\Desktop\closurv\offline"')
    if opt == 2:
        sync_win = Toplevel(root)
        sync_win.title("Sync Files")
        sync_win.geometry("400x400")
        sync_win.minsize(400, 400)
        sync_win.maxsize(400, 400)


menubar = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Sync', menu=file)
file.add_command(label='Explore Files', command=lambda: cloud_menu(1))
file.add_command(label='Sync Files', command=lambda: cloud_menu(2))
root.config(menu=menubar)


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 3306), 2)
        s.close()
        return True
    except:
        pass
    return False


def main_method():
    global framecount1
    try:
        mydb = mysql.connector.connect(
            host="dummy",
            user="nishantj_user1",
            database="nishantj_db1",
            password="dummy"
        )
    except:
        pass
    while(True):
        x = datetime.datetime.now()
        # Capture frame-by-frame
        success, image = cap1.read()
        framecount1 += 1

        # Check if this is the frame closest to 10 seconds
        if framecount1 == (framerate1 * 10):
            framecount1 = 0
            name = "frame"+(x.strftime("%f"))+".jpg"
            path = "offline/indoor/"+name
            cv2.imwrite(path, image)  # 'frame%d.jpg'%int(x.strftime("%f"))
            # if internet is there
            is_conn = is_connected(REMOTE_FTP_SERVER)
            if is_conn:
                try:
                    print("file name:" + path)
                    file = open(path, 'rb')
                    print("file opened")            # file to send
                    ind_ftp_sess.storbinary(
                        'STOR '+name, file)     # send the file
                    print("file sent")
                    file.close()
                    mycursor = mydb.cursor()
                    # mycursor.execute("CREATE TABLE customers(name VARCHAR(100), address VARCHAR(100));")
                    sql = ("INSERT INTO customers (name, address) VALUES (%s,%s)")
                    val = ("Felix", name)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    os.remove(path)
                except ftplib.all_errors as e:
                    print("FTP ERROR FOR INDOOR: "+e.msg)
                    # save to offline dir
                except mysql.connector.Error as e:
                    print("mysql error in indoor: " + e.msg)

            else:
                # save to offline dir
                pass
        # Check end of video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # cv2.imshow("Frame", image)


start_butt = Button(start_frame, text="Start", width=25, command=main_method)
start_butt.grid(row=5, column=1, sticky=W, pady=10)
root.mainloop()
