#!/usr/bin/env python
'''
The code will run on the receiver side
will receive the data from the stream server
Pure Python Socket program, without using ROS platform
Purpose: To test the transmission rate and latency vs runing on ROS
'''
import cv2
from socket import *
import base64
import numpy as np
import blosc
import time
import zlib
from PIL import Image
import StringIO


if __name__ == '__main__':
    PORT = 3030  # default 5000 for both sides
    s = socket(AF_INET, TCP_NODELAY)
    s.bind(('', PORT))
    s.listen(5)
    BUFSIZE = 300000  # should be 2^n


    count = 0
    lasttime = int(round(time.time() * 1000))

    while True:
        try:
            conn, (host, remoteport) = s.accept()
            arr1 = b""
            while True:
                data = conn.recv(BUFSIZE)
                if not data:
                    break
                arr1 += data

            #data = zlib.decompress(arr1)

            #data = np.fromstring(data, dtype=np.uint8).reshape(240,320,3)
            rgb = Image.open(StringIO.StringIO(zlib.decompress(arr1)))
            rgb = np.array(rgb)

            conn, (host, remoteport) = s.accept()
            arr1 = b""
            while True:
                data = conn.recv(BUFSIZE)
                if not data:
                    break
                arr1 += data
            #depth = Image.open(StringIO.StringIO(arr1))
            #depth = np.array(depth)
            depth = zlib.decompress(arr1)
            depth = np.fromstring(depth, dtype=np.uint8).reshape(480,640)
            d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

            cv2.imshow('Color', np.hstack((rgb,d4d)))
            #data = np.fromstring(data, dtype=np.uint8).reshape(240,320,4)
            #data = np.dsplit(data,[3])
            #rgb = data[0]
            #depth = data[1].reshape(240,320)
            #d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
            #cv2.imshow('Depth || Color', np.hstack((rgb,d4d)))


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if (int(round(time.time() * 1000)) - lasttime > 10000):
                lasttime = int(round(time.time() * 1000))
                print("Average FPS:" + str(count / 10.0))
                count = 0
            count += 1

        except Exception as e:
            print "[Error] " + str(e)

    connection.close()
