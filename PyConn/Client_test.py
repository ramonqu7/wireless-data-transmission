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
        self.device = openni2.Device.open_any()

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

    def initDepth(self,x,y,fps):
        self.depth_stream = self.device.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=x,
                               resolutionY=y, fps=fps))
        self.depth_stream.set_mirroring_enabled(True)
        self.depth_stream.start()

    def initColor(self,x,y,fps):
        self.rgb_stream = self.device.create_color_stream()
        self.rgb_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=x,
                               resolutionY=y, fps=fps))







