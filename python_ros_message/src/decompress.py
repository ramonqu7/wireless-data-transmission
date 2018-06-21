#!/usr/bin/env python3
import message_filters
from sensor_msgs.msg import Image
from rgbd_compress.msg import Rgbd
import rospy
import zlib
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from cv_bridge import CvBridge, CvBridgeError

RGB_COMPRESS = 75

def parseColor(rgbd):
    temp = rgbd.find(b'ColDep')
    rgb = rgbd[:temp]
    depth = rgbd[temp+1:]
    return BytesIO(rgb), zlib.decompress(depth)


def callback(rgbd):
    global sub, bridge, RGB_COMPRESS,rgb_pub, dep_pub
    rgb_data,dep_data = parseColor(rgbd.data)

    rgb_msg = Image()
    rgb_msg.header = rgbd.header
    rgb_msg.data = cv2.cvtColor(np.asarray(Image.open(rgb_data)), cv2.COLOR_RGB2BGR)



    dep_msg = Image()
    dep_msg.header = rgbd.header
    dep_msg.data = np.fromstring(dep_data,dtype=np.uint8).reshape(480,640)





if __name__ == '__main__':
    bridge = CvBridge()

    rospy.init_node('Joule', anonymous=True)
    sub = rospy.Subscriber('/camera.rgbd',Rgbd, callback)

    rgb_pub = rospy.Publisher('camera/rgb', Image,queue_size=20)
    dep_pub = rospy.Publisher('camera/depth', Image,queue_size=20)
    

    rospy.spin()