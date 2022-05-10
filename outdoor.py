# install opencv "pip install opencv-python"
import cv2
import datetime
import socket
import os
import mysql.connector
import ftplib
import threading


try:
    ind_ftp_sess = ftplib.FTP('ftp.nishantjoshi.tech',
                              'outdoor@nishantjoshi.tech', 'ftpadmin')
except:
    pass
REMOTE_FTP_SERVER = "ftp.nishantjoshi.tech"

try:
    mydb = mysql.connector.connect(
        host="212.1.210.79",
        user="nishantj_dbuser",
        database="nishantj_MH05EJ4657",
        password="admin"
    )
except:
    print("mysql conn error")
    pass


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


def captur(path, name):
    try:
        mydb = mysql.connector.connect(
            host="212.1.210.79",
            user="nishantj_outdoor",
            database="nishantj_MH05EJ4657",
            password="admin"
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
            "INSERT INTO tabout (imgname, imgyr, imgmon, imgdate, imgday, imghr, imgmin, imgsec,vnum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
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


# distance from camera to object(face) measured
# centimeter
Known_distance = 100

# width of face in the real world or Object Plane
# centimeter
Known_width = 14.3

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# focal length finder function


def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

# distance estimation function


def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):

    distance = (real_face_width * Focal_Length)/face_width_in_frame

    # return the distance
    return distance


def face_data(image):

    face_width = 0  # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:

        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel

    return face_width


# reading reference_image from directory
ref_image = cv2.imread("REF.jpeg")

# find the face width(pixels) in the reference_image
ref_image_face_width = face_data(ref_image)
print(ref_image_face_width)
# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)

print(Focal_length_found)

# show the reference image
# cv2.imshow("ref_image", ref_image)

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(3)
framerate = cap.get(cv2.CAP_PROP_FPS)
framecount = 0
# looping through frame, incoming from
# camera/video
while True:

    # reading the frame from camera
    _, frame = cap.read()

    # calling face_data function to find
    # the width of face(pixels) in the frame
    face_width_in_frame = face_data(frame)

    # check if the face is zero then not
    # find the distance
    if face_width_in_frame != 0:

        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)

        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

        # Drawing Text on the screen
        cv2.putText(
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),
            fonts, 0.6, GREEN, 2)
        if (round(Distance, 2) < 80.00):
            framecount += 1
            print(framecount)
            # Check if this is the frame closest to 10 seconds
            if framecount == (framerate * 5):
                framecount = 0
                x = datetime.datetime.now()
                name = "frame"+(x.strftime("%f"))+".jpg"
                path = "offline/outdoor/"+name
                cv2.imwrite(path, frame)
                is_conn = is_connected(REMOTE_FTP_SERVER)
                if is_conn:
                    t = threading.Thread(target=lambda: captur(path, name))
                    t.daemon = True
                    t.start()

        else:
            framecount = 0
    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()

# closing the the windows that are opened
cv2.destroyAllWindows()
