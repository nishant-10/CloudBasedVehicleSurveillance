import mysql.connector
import datetime
import ftplib
import cv2
import socket
import os
import timedb
import multiprocessing
from tkinter import *
cap1 = cv2.VideoCapture(3)
framerate1 = cap1.get(cv2.CAP_PROP_FPS)
framecount1 = 0
APP_STAT = True
try:
    ind_ftp_sess = ftplib.FTP('ftp.dummy',
                              'indoor@dummy', 'ftpdummy')
except:
    pass
REMOTE_FTP_SERVER = "ftp.dummy"


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
    global framecount1, ind_ftp_sess
    try:
        mydb = mysql.connector.connect(
            host="dummy",
            user="nishantj_dbuser",
            database="nishantj_MH05EJ4657",
            password="dummy"
        )
    except:
        pass
    while(True) and APP_STAT == True:
        x = datetime.datetime.now()
        # Capture frame-by-frame
        success, image = cap1.read()
        cv2.imshow("Frame", image)
        framecount1 += 1

        # Check if this is the frame closest to 10 seconds
        if framecount1 == (framerate1 * 10):
            framecount1 = 0
            name = "frame"+(x.strftime("%f"))+".jpg"
            path = "offline/indoor/"+name
            cv2.imwrite(path, image)  # 'frame%d.jpg'%int(x.strftime("%f"))
            t = datetime.datetime.now()
            db_y = int(t.strftime("%Y"))
            db_mth = t.strftime("%B")
            db_day = t.strftime("%A")
            db_dat = int(t.strftime("%d"))
            db_min = int(t.strftime("%M"))
            db_hr = int(t.strftime("%H"))
            db_sec = int(t.strftime("%S"))
            db_vnum = "MH05EJ4657"
            print(db_sec)
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
                    print("sql started")
                    mycursor = mydb.cursor()
                    # mycursor.execute("CREATE TABLE customers(name VARCHAR(100), address VARCHAR(100));")
                    sql = (
                        "INSERT INTO tabind (imgname, imgyr, imgmon, imgdate, imgday, imghr, imgmin, imgsec,vnum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")

                    val = (name, db_y, db_mth, db_dat,
                           db_day, db_hr, db_min, db_sec, db_vnum)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("sql sent")
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
        # closing the camera


t1 = None


def thread1():
    t1 = multiprocessing.Process(target=main_method())
    t1.start()


def app_stop():
    APP_STAT = False
    cap1.release()
    cv2.destroyAllWindows()


root = Tk()
root.title("Indoor Surv")
root.geometry('200x200')
Start_butt = Button(root, text="Start", command=thread1)
Stop_butt = Button(root, text="Stop", command=app_stop)
Start_butt.grid(row=0, column=0)
Stop_butt.grid(row=1, column=0)
root.mainloop()
