import threading
import sys, time
from socket import *
import pickle
import numpy as np
import cv2
from primesense import openni2#, nite2
from primesense import _openni2 as c_api


class Client:
    def __init__(self):
        self.BUFSIZE = 10000
        self.hostAddr = "192.168.137.1"
        self.PORT = 5000
        self.dist = '/home/test/Desktop/OpenNI-Linux-x64-2.2/Redist/'

    def setAddr(self,addr):
        self.hostAddr = addr

    def setDist(self,dist):
        self.dist = dist

    def initRun(self):
        openni2.initialize(self.dist)
        if (openni2.is_initialized()):
            print("openNI2 initialized")
        else:
            print("openNI2 not initialized")



