import os
import time
import random
import threading
import sys, time
from socket import *
import pickle
import numpy as np
import cv2
import zlib
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

ser_run = True
BUFSIZE = 10000
hostAddr = "192.168.137.250"
PORT = 5000
def ser():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(5)
    print("listening...")
    n = 0
    while True:
        conn, (host, remoteport) = s.accept()
        #size = conn.recv(BUFSIZE)
    #receive one number (the size of the array

        arr1 = b""
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            #parse the data and show the image
            arr1+=(data)

    #canvas = np.hstack((rgbd))


        arr1 = np.fromstring(zlib.decompress(arr1),dtype=np.uint8).reshape(480,640,3)
        n+=1
    ## Distance map print('Center pixel is {} mm away'.format(dmap[119, 159]))

    ## Display the stream
        cv2.imshow('depth', arr1)
        cv2.waitKey(1)


        conn.close()

def start_ser():

        thread = threading.Thread(target=ser)
        thread.start()
start_ser()