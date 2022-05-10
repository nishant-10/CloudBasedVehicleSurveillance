from tkinter import *
from tkinter import messagebox
import os
import ftplib
import socket
import mysql.connector
import datetime
import subprocess
sync_win = Tk()
sync_win.title("Sync Files")
sync_win.geometry("400x400")
sync_win.minsize(400, 400)
sync_win.maxsize(400, 400)

status_lbl = Label(sync_win, text="Loading...", bd=1,
                   relief=SUNKEN, width=40, anchor=W, pady=5)
scrollbar = Scrollbar(sync_win)
try:
    ind_ftp_sess = ftplib.FTP('ftp.dummy',
                              'indoff@dummy', 'ftpdummy')
    out_ftp_sess = ftplib.FTP('ftp.dummy',
                              'outoff@dummy', 'ftpdummy')
    drivdata_ftp_sess = ftplib.FTP('ftp.dummy',
                                   'drivdataoff@dummy', 'ftpdummy')
except:
    pass
REMOTE_FTP_SERVER = "ftp.dummy"


def is_connected(hostname1):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname1)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 3306), 2)
        s.close()
        return True
    except:
        pass
    return False


def fupload(name, path, opt):
    global ind_ftp_sess, out_ftp_sess, drivdata_ftp_sess, REMOTE_FTP_SERVER, REMOTE_FTP_SERVER2
    if opt == 1:
        sess = ind_ftp_sess
    if opt == 2:
        sess = out_ftp_sess
    if opt == 3:
        sess = drivdata_ftp_sess

    if is_connected(REMOTE_FTP_SERVER):
        try:
            mydb = mysql.connector.connect(
                host="dummy",
                user="nishantj_filesync",
                database="nishantj_MH05EJ4657",
                password="dummy"
            )

            print("file name:" + path)
            file = open(path, 'rb')
            print("file opened")            # file to send
            sess.storbinary(
                'STOR '+name, file)     # send the file
            print("file sent")
            file.close()
            print("sql started")
            mycursor = mydb.cursor()
            # mycursor.execute("CREATE TABLE customers(name VARCHAR(100), address VARCHAR(100));")
            sql = (
                "INSERT INTO taboff (imgname, imgyr, imgmon, imgdate, imgday, imghr, imgmin, imgsec,vnum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            t = datetime.datetime.now()
            db_y = int(t.strftime("%Y"))
            db_mth = t.strftime("%B")
            db_day = t.strftime("%A")
            db_dat = int(t.strftime("%d"))
            db_min = int(t.strftime("%M"))
            db_hr = int(t.strftime("%H"))
            db_sec = int(t.strftime("%S"))
            db_vnum = "MH05EJ4657"
            val = (name, db_y, db_mth, db_dat,
                   db_day, db_hr, db_min, db_sec, db_vnum)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            print("sql sent")
            os.remove(path)
        except ftplib.all_errors as e:
            print("FTP ERROR FOR DRIVERDATA: "+e.msg)
            # save to offline dir
        except mysql.connector.Error as e:
            print("mysql error in DRIVERDATA: " + e.msg)
    else:
        messagebox.showinfo(
            "Internet", "No Internet Connection.")


def sync_files():
    global REMOTE_FTP_SERVER
    if is_connected(REMOTE_FTP_SERVER):
        if (len(os.listdir('offline/indoor'))) > 0:
            for name in os.listdir('offline/indoor'):
                print(name)
                path = "offline/indoor/"+name
                fupload(name, path, 1)

        if (len(os.listdir('offline/outdoor'))) > 0:
            for name in os.listdir('offline/outdoor'):
                print(name)
                path = "offline/outdoor/"+name
                fupload(name, path, 2)

        if (len(os.listdir('offline/driverdata'))) > 0:
            for name in os.listdir('offline/driverdata'):
                print(name)
                path = "offline/driverdata/"+name
                fupload(name, path, 3)
    else:
        messagebox.showinfo(
            "Internet", "No Internet Connection.")


start_butt = Button(sync_win, text="Start Sync", width=20,
                    command=sync_files)


def file_status():
    global status_lbl, sync_win
    ind_files = os.listdir('offline/indoor')
    out_files = os.listdir('offline/outdoor')
    dd_files = os.listdir('offline/driverdata')
    if len(ind_files) or len(out_files) or len(dd_files) > 0:
        status_lbl['text'] = "Indoor : Files to sync : " + \
            str(len(ind_files))+"\n"
        status_lbl['text'] += "Outoor : Files to sync : " + \
            str(len(out_files))+"\n"
        status_lbl['text'] += "Driver data : Files to sync : " + \
            str(len(dd_files))

    else:
        status_lbl.config(text="No files found")
        start_butt.config(state=DISABLED)
        messagebox.showinfo(
            "Sync Offline Files", "No offline data found.\nIt is either already synced or was deleted manually.\nSelect Sync > Explore Files from the main window.")


def open_exp():
    subprocess.Popen(
        r'explorer /select,"C:\Users\91882\Desktop\closurv\offline"')


exp_butt = Button(sync_win, text="Open File Location",
                  width=20, command=open_exp)
status_lbl.grid(row=0, column=0, columnspan=3)
start_butt.grid(row=2, column=1, padx=128, pady=10)
exp_butt.grid(row=3, column=1, padx=128, pady=10)
file_status()
sync_win.mainloop()
