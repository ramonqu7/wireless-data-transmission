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
        self.s = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM -> TCP connection
    #Server Address Setter
    def setAddr(self,addr):
        self.hostAddr = addr
    #local directory for Openni2 driver
    def setDist(self,dist):
        self.dist = dist
    #initially run the openni2 driver
    def initRun(self):
        openni2.initialize(self.dist)
        if (openni2.is_initialized()):
            print("openNI2 initialized")
        else:
            print("openNI2 not initialized")
    #setting for depth camera
    def initDepth(self,x,y,fps):
        self.depth_stream = self.device.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=x,
                               resolutionY=y, fps=fps))
        self.depth_stream.set_mirroring_enabled(True)
        self.depth_stream.start()
    #settings for color camera
    def initColor(self,x,y,fps):
        self.rgb_stream = self.device.create_color_stream()
        self.rgb_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=x,
                               resolutionY=y, fps=fps))
        self.rgb_stream.start()
    #get depth 1d array
    def getDepth(self,x,y):
        self.data = np.fromstring(self.depth_stream.read_frame().get_buffer_as_uint16(),
                                  dtype=np.uint16).reshape(y,x)
    #the base to send the data to the server
    def send(self,data):

        self.s.sendto(data,(self.hostAddr,self.PORT))

    #the prepare the data(in the future compress or define own packet type
    def prepareData(self,rawData):
        return rawData.tostring()

    def show(self):
        d4d = np.uint8(self.data.astype(float) * 255 / 2 ** 12 - 1)
        # Correct the range. Depth images are 12bits
        self.d4d = 255 - cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)


    def run(self):
        self.initRun()
        self.initDepth(640,480,30)

        done = False
        self.s.connect((self.hostAddr, self.PORT))
        while not done:
            key = cv2.waitKey(1) & 255
            ## Read keystrokes
            if key == 27:  # terminate
                print("\tESC key detected!")
                done = True
            '''elif chr(key) == 's':  # screen capture
                print("\ts key detected. Saving image and distance map {}".format(s))
                np.savetxt("ex5dmap_" + str(s) + '.out', dmap)
                # s+=1 # uncomment for multiple captures '''
            self.getDepth(640,480)
            self.send(self.prepareData(self.data))

            self.show()
            cv2.imshow("depth", self.d4d)

            ## Distance map
            # print('Center pixel is {} mm away'.format(dmap[119, 159]))
        cv2.destroyAllWindows()
        self.depth_stream.stop()
        openni2.unload()
        self.s.close()
        print("Terminated")

if __name__ == '__main__':
    c = Client()
    c.run()













