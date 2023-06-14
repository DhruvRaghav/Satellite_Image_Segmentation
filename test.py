# from system import time
# import time
import datetime
# print(datetime.datetime.now())

import os, time, sys

path = "/home/ceinfo/Desktop/Sonepat_50m/"
now = time.time()
# print(now)

for f in os.listdir("/home/ceinfo/Desktop/Sonepat_50m/"):
    print( f )
    f = os.path.join(path, f)

    if os.stat(f).st_mtime < now - 1 * 86400:
        if os.path.isfile(f):
            os.remove(os.path.join(path, f))