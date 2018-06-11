#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image, CompressedImage
import threading
import time
import zlib

import bz2
from std_msgs.msg import Int16MultiArray,String, Header
import cv2
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sys import argv
import json

count = 0
lasttime = 0
latency = 0
bridge = CvBridge()
fps = []
lat = []

count1 = 0
latency1 = 0
lasttime1 = 0
fps1 = []
lat1 = []

# video recorder
fourcc = cv2.VideoWriter_fourcc('M','J','P','G') # cv2.VideoWriter_fourcc() does not exist
video_writer = cv2.VideoWriter("output_2.avi", fourcc, 30, (640, 480))
video_writer1 = cv2.VideoWriter("output_21.avi", fourcc, 30, (640, 480))

#To parse the command line arguments
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def parseData(data):
    #frame = zlib.decompress(data)
    frame = np.fromstring(data, dtype=np.uint16).reshape(480, 640)
    d4d = frame
    d4d = np.uint8(frame.astype(float) * 255 / 2 ** 12 - 1)
    d4d = 255 - cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
    return d4d

def ShowCompressedImage(data):
    np_arr = np.fromstring(data.data, np.uint8)
    #print(np_arr.shape)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image_np

def ShowImage(data):
    global bridge
    try:
         cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
         print(cv_image.shape)
         return cv_image
    except CvBridgeError as e:
         print(e)


def ShowDepth(data):
    global bridge
    try:
         data.encoding = "mono16"
         cv_image = bridge.imgmsg_to_cv2(data, "mono8")
         return cv_image
    except CvBridgeError as e:
         print(e)
def ShowCompressedDepth(data):
    np_arr = np.fromstring(data.data, np.uint8)

    image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    image_np =cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)

    return image_np

def callback(data):
    global count, lasttime,latency,fps,lat,video_writer,video_writer1
    #rospy.loginfo(rospy.get_caller_id() + "I heard")
    try:
        #cv2.namedWindow("Color", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("Color", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
        cv2.waitKey(1) & 255
        frame = ShowCompressedImage(data)
        video_writer.write(frame)
        cv2.imshow("Color", frame)
    except:
        pass
    #ShowCompressedImage(data)
    #ShowImage(data)
    #timestamp = data.header.stamp
    #latency += time.time() - (timestamp.secs+round((timestamp.nsecs/ 1000000000.0),5))



def callback1(data):
    global count1, lasttime1,latency1,fps1,lat1,video_writer1,video_writer
    try:
            #cv2.namedWindow("Depth", cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty("Depth", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
            #cv2.waitKey(1) & 255
            frame = ShowCompressedDepth(data)
            video_writer1.write(frame)
            #cv2.imshow("Depth", frame)
    except:
            pass
        #rospy.loginfo(rospy.get_caller_id() + "I heard")
        #cv2.waitKey(1) & 255
        #cv2.imshow("Depth", ShowCompressedDepth(data))
        #ShowCompressedDepth(data)

def listener():
    global count, lasttime,latency,bridge,lasttime1, video_writer

    try:

        # In ROS, nodes are uniquely named. If two nodes with the same
        # node are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('listener', anonymous=False, disable_signals=True)
        lasttime = int(round(time.time() * 1000))
        lasttime1 = int(round(time.time() * 1000))
        rospy.Subscriber("/camera/color/image_raw/compressed", CompressedImage, callback,  queue_size = 1)
        rospy.Subscriber("/camera/depth/image_rect_raw/compressed", CompressedImage, callback1,  queue_size = 1)
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()
    except:
                video_writer.release()
                video_writer1.release()
                cv2.destroyAllWindows()


if __name__ == '__main__':
    myargs = getopts(argv)
    listener()
