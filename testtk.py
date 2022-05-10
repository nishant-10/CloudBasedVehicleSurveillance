import os
import socket
import ftplib
imgname = "animal.jpg"

# 212.1.210.79
REMOTE_SERVER = "ftp.nishantjoshi.tech"


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 3306), 2)
        try:
            # ftpupload code goes below this
            # delete files
            try:
                os.remove('testimg/'+imgname)
                print("image deleted")
            except OSError as e:
                print(e)

        except ftplib.all_errors as e:
            # do not delete files
            print(e)
            pass
        s.close()
        return True
    except:
        print("no internet")
        pass
    return False


print(is_connected(REMOTE_SERVER))
