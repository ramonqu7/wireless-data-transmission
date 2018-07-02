#!/usr/bin/env python
'''
The code will run on the Transmitter side (Joule)
will stream the video data from the camera
Pure Python Socket program, without using ROS platform
Purpose: To test the transmission rate and latency vs runing on ROS
'''
from openni2_device_init import visionsensor
import time
import json
from socket import *
import base64
import numpy as np
import blosc
from threading import Thread
import cv2


SERVER_IP = "69.91.157.166"
SERVER_PORT = 1080
MAX_NUM_CONNECTIONS = 5


class ConnectionPool(Thread):

    def __init__(self):
        #Thread.__init__(self)
        self.BUFSIZE = 10000
        self.hostAddr = "173.250.152.233"
        self.PORT = 5000

        self.device = visionsensor()
        self.initDevice()


    def initDevice(self):
        self.device.createColor()
        self.device.createDepth()
        self.device.sync()
        self.device.startColor()
        self.device.startDepth()

    def getData(self):
        rgb = self.device.getRgb()
        depth = self.device.getDepth2Gray(self.device.getDepth2Int8())
        #tarray = np.dstack((rgb,depth))
        return rgb, depth

    def send(self,data):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.hostAddr, self.PORT))
        self.s.sendto(data,(self.hostAddr,self.PORT))
        self.adata = len(data)
        print("Pre:"+str(self.ndata)+" After: "+str(self.adata)+" rate"+str(round(self.adata*1.0/self.ndata*100)))
        self.s.close()

    def getImage(self):
        try:
            n = 0
            while n<3000:
                n+=1
                rgb,depth = self.getData()
                #self.ndata = len(data)
                #data = blosc.compress(data,cname='zlib')
                #self.send(data)
                print(n)
                cv2.imwrite("./pic/rgb_"+str(n)+".png",rgb)
                cv2.imwrite("./pic/depth_"+str(n)+".png",depth)

        except Exception, e:
            print "[Error] " + str(e.message)



if __name__ == '__main__':
        #thread = ConnectionPool()
        #thread.start()
        a = ConnectionPool()
        a.getImage()
