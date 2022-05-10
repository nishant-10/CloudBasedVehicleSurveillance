from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import ftplib
import cv2
import socket
import os
import mysql.connector
import datetime
import threading
from pygame import mixer
duration = 1000  # milliseconds
freq = 440  # Hz
mixer.init()
sound = mixer.Sound("siren.wav")
try:
    ind_ftp_sess = ftplib.FTP('ftp.dummy',
                              'dummy', 'dummy')
except:
    pass
REMOTE_FTP_SERVER = "ftp.dummy"

try:
    mydb = mysql.connector.connect(
        host="dummy",
        user="nishantj_dbuser",
        database="nishantj_MH05EJ4657",
        password="dummy"
    )
except:
    print("mysql conn error")
    pass


def one():
    os.system('python sms.py')


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


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
# Dat file is the crux of the code
# C:/Users/91882/Desktop/closurv/shape_predictor_68_face_landmarks.dat
predict = dlib.shape_predictor(
    "C:/Users/91882/Desktop/closurv/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = cv2.VideoCapture(3)
framerate = cap.get(cv2.CAP_PROP_FPS)
framecount = 0
print("framerate:"+str(framerate))
flag = 0


def captur(path, name):
    try:
        mydb = mysql.connector.connect(
            host="dummy",
            user="nishantj_drivdata",
            database="nishantj_MH05EJ4657",
            password="dummy"
        )

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
            "INSERT INTO tabdrivdata (imgname, imgyr, imgmon, imgdate, imgday, imghr, imgmin, imgsec, vnum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
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
        t1 = threading.Thread(target=one)
        t1.daemon = True
        t1.start()
    except ftplib.all_errors as e:
        print("FTP ERROR FOR DRIVERDATA: "+e.msg)
        # save to offline dir
    except mysql.connector.Error as e:
        print("mysql error in DRIVERDATA: " + e.msg)


while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < thresh:
            flag += 1
            # print(flag)
            if flag >= frame_check:
                cv2.putText(frame, "****************ALERT!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "****************ALERT!****************", (10, 325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                framecount += 1
                # print(framecount)
                if framecount == (framerate * 3):
                    sound.play()
                    # print("framerate:"+framerate)
                    framecount = 0
                    t = datetime.datetime.now()
                    name = "frame"+(t.strftime("%f"))+".jpg"
                    path = "offline/driverdata/"+name
                    cv2.imwrite(path, frame)
                    is_conn = is_connected(REMOTE_FTP_SERVER)
                    if is_conn:
                        t = threading.Thread(target=lambda: captur(path, name))
                        t.daemon = True
                        t.start()

                    print("SLEPT")
        else:
            flag = 0
            framecount = 0
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.release()
