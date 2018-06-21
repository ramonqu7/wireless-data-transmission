#!/usr/bin/env python3
import message_filters
import sensor_msgs.msg 
from rgbd_compress.msg import rgbd
import rospy
import zlib
import numpy as np
import Image
from io import BytesIO
import cv2
from cv_bridge import CvBridge, CvBridgeError

RGB_COMPRESS = 75

def parseColor(rgbd):
    temp = rgbd.find(b'ColDep')
    rgb = rgbd[:temp]
    depth = rgbd[temp+6:]
    return BytesIO(rgb), zlib.decompress(depth)


def callback(rgbd):
    global sub, bridge, RGB_COMPRESS,rgb_pub, dep_pub
    rgb_data,dep_data = parseColor(rgbd.data)

    rgb_msg = bridge.cv2_to_imgmsg(cv2.cvtColor(np.asarray(Image.open(rgb_data)), cv2.COLOR_RGB2BGR),"rgb8")
    rgb_msg.header = rgbd.header
    rgb_msg.encoding = "rgb8"
    rgb_msg.step = 1920
    rgb_msg.width = 640
    rgb_msg.height = 480

    rgb_pub.publish(rgb_msg)


    dep_msg = bridge.cv2_to_imgmsg(np.fromstring(dep_data,dtype=np.uint16).reshape(480,640), "16UC1")
    dep_msg.header = rgbd.header
    dep_msg.encoding = "16UC1"
    dep_msg.step = 1280
    dep_msg.width = 640
    dep_msg.height = 480

    dep_pub.publish(dep_msg)



if __name__ == '__main__':
    bridge = CvBridge()
    rospy.init_node('DeCompressor', anonymous=False)
    sub = rospy.Subscriber('/camera/rgbd',rgbd, callback)
    rgb_pub = rospy.Publisher('camera/rgb/decompress', sensor_msgs.msg.Image,queue_size=20)
    dep_pub = rospy.Publisher('camera/depth/decompress', sensor_msgs.msg.Image,queue_size=20)
    rospy.spin()