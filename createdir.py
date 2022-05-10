import os
CHECK_DIR1 = 'offline'
CHECK_DIR2 = 'offline/indoor'
CHECK_DIR3 = 'offline/outdoor'
CHECK_DIR4 = 'offline/driverdata'


def check_folders():
    if(os.path.isdir(CHECK_DIR1)) == False:
        os.mkdir('offline')
        os.mkdir('offline/indoor')
        os.mkdir('offline/outdoor')
        os.mkdir('offline/driverdata')

    if(os.path.isdir(CHECK_DIR2)) == False:
        os.mkdir('offline/indoor')
    if(os.path.isdir(CHECK_DIR3)) == False:
        os.mkdir('offline/outdoor')
    if(os.path.isdir(CHECK_DIR4)) == False:
        os.mkdir('offline/driverdata')
