import os
import time
import random
import threading
import sys, time
from socket import *
import pickle
import numpy as np
import cv2
from primesense import openni2  # , nite2
from primesense import _openni2 as c_api
import zlib

ser_run = True
BUFSIZE = 8192
hostAddr = "192.168.137.1"
PORT = 5000




n = 0
s = socket(AF_INET, TCP_NODELAY)


def cli_send(arr1):
    global s

    # send the size of the array
    # s.send(arr1.size)
    # send the combined version of the array (for rgbd)
    s.sendto(zlib.compress(arr1.tostring()), (hostAddr, PORT))
    # with open("testSend.txt","ab") as f:


# f.write(zlib.compress(arr1.tostring()))


def cli_send1(arr1):
    global s

    # send the size of the array
    # s.send(arr1.size)
    # send the combined version of the array (for rgbd)
    t = str(int(round(time.time() * 1000)))[-4:]
    data = t + arr1.tostring()
    data = zlib.compress(data)

    s.sendto(data, (hostAddr, PORT))


def cli_send2(arr1):
    global s
    # send the size of the array
    data = arr1.tostring()
    data = zlib.compress(data) + b"END"

    s.send(data)


'''
done = False
while not done:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((hostAddr, PORT))
    key = cv2.waitKey(1) & 255
    ## Read keystrokes
    if key == 27:  # terminate
        print("\tESC key detected!")
        done = True
    elif chr(key) == 's':  # screen capture
        print("\ts key detected. Saving image and distance map {}".format(s))
        np.savetxt("ex5dmap_" + str(s) + '.out', dmap)
        # s+=1 # uncomment for multiple captures
    # if

    ## Streams

    # DEPTH
    dmap, d4d = get_depth()

    cli_send(dmap)
    s.close()

    cv2.imshow("depth",d4d)



    ## Distance map
    # print('Center pixel is {} mm away'.format(dmap[119, 159]))


# end while
'''
while True:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((hostAddr, PORT))
    # while True:
    dmap, d4d = get_depth()
    # cv2.imshow("dd",d4d)
    # cv2.waitKey(1)&255

    cli_send(dmap)
    s.close()

## Release resources
depth_stream.stop()
openni2.unload()
print("Terminated")


