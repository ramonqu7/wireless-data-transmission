#!/usr/bin/env python
from openni2_device_init import VisionSensor
import rospy
from std_msgs.msg import Int16MultiArray
import time
import zlib
import rospy
import cv2

class RgbdPublisher:
    def __init__(self):
        self.device = VisionSensor()
        self.device.createDepth() # default 640*480*30fps
        self.RosInit()

    def RosInit(self):
        self.node = rospy.Publisher('CameraTest',Int16MultiArray, queue_size=30)
        rospy.init_node("Joule", anonymous=False)

    def publishFrame(self):
      #while True:
      while not rospy.is_shutdown():
        self.device.getDepth()
        data = self.device.converDepth2Gray()
        self.node.publish(data)
        #cv2.imshow("Depth",data)
        #cv2.waitKey(1)&255


if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
        rgbd.publishFrame()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")
