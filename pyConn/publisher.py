#!/usr/bin/env python
from openni2_device_init import visionsensor
import rospy
from std_msgs.msg import String
import time
import rospy
import cv2
import numpy as np
import zlib
import scipy.ndimage
import thread
from PIL import Image
from io import BytesIO

class RgbdPublisher:
    def __init__(self):
        self.device = visionsensor()
        self.device.createDepth() # default 640*480*30fps
        self.device.createColor() # default 640*480*30fps
        self.device.sync()
        self.device.startColor()
        self.device.startDepth()
        time.sleep(1)
        self.RosInit() #init the cameras and ros node


    def RosInit(self):
        #self.depth = rospy.Publisher('Depth',String, queue_size=30)
        self.rgbd = rospy.Publisher('RGBD', String, queue_size=30)
        rospy.init_node("Joule", anonymous=False)

    def getData(self):
        rgb = self.device.getRgb()
        depth = self.device.getDepth2Int8()
        #tarray = np.dstack((rgb,depth))
        return rgb, depth

    def publishFrame(self):
        #while True:
        #self.temp = np.zeros((480*640*4),dtype=np.uint8)
        while not rospy.is_shutdown():

            try:
                if(self.rgbd.get_num_connections()> 0):
                    rgb, depth = self.getData()
                    img = Image.fromarray(rgb)
                    #img1 = Image.fromarray(depth)
                    fpath =BytesIO()
                    img.save(fpath, quality = 75, format = "JPEG")
                    #img.save("rgb.jpg",quality = 75)
                    fpath.seek(0)
                    self.rgbd.publish(zlib.compress(fpath.getvalue()))
                    #dpath = BytesIO()
                    #img1.save(dpath, quality = 75, format = "JPEG")
                    #dpath.seek(0)
                    data = depth.tostring()

                    self.rgbd.publish(zlib.compress(data))

                    #d4d = self.device.getDepth2Gray()

                    #self.node_c.publish(self.device.getRgbd())
                    #cv2.imshow("depth",d4d)
                    #cv2.waitKey(1)&255
            except Exception,e:
                if e == KeyboardInterrupt:
                    break

        self.device.stopDepth()
        self.device.stopColor()





if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
        rgbd.publishFrame()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")

'''
Seperate to multiple topics
rgb = self.device.getRgb()
r,g,b = np.split(rgb,3, axis=2)
r = np.squeeze(r)
g = np.squeeze(g)
b = np.squeeze(b)
d = self.device.getDepth2Int8()
#tarray = np.append(rgb,depth)
self.r.publish(blosc.compress(r.tostring()))
self.g.publish(blosc.compress(g.tostring()))
self.b.publish(blosc.compress(b.tostring()))
self.d.publish(blosc.compress(d.tostring()))

'''
