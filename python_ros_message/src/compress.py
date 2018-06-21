#!/usr/bin/env python3
import message_filters
from sensor_msgs.msg import Image
from rgbd_compress.msg import rgbd
import rospy
import zlib
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

RGB_COMPRESS = 75

def callback(rgb, dep):
    global pub, bridge, RGB_COMPRESS
    rgbd_msg = rgbd()
    rgbd_msg.header = dep.header

    try:
        rgb_data = bridge.imgmsg_to_cv2(rgb , "rgb8")
    except CvBridgeError as e:
        print(e)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), RGB_COMPRESS]
    ret, rgb_compressed = cv2.imencode('.jpg', rgb_data, encode_param)
    rgb_compressed = rgb_compressed.tobytes()

    try:
        dep_data = bridge.imgmsg_to_cv2(dep , "16UC1")  #may not be brg8
    except CvBridgeError as e:
        print(e)
    #Trim down to 1d Array
    dep_compressed = zlib.compress(dep_data)

    final_compressed = rgb_compressed + b'ColDep'+ dep_compressed

    rgbd_msg.data = final_compressed

    pub.publish(rgbd_msg)


'''
        if self.depth:
            depth = zlib.compress(self.device.getDepth2Int8())
'''




if __name__ == '__main__':
    bridge = CvBridge()

    rgb_sub = message_filters.Subscriber('/camera/color/image_raw', Image)
    dep_sub = message_filters.Subscriber('/camera/aligned_depth_to_color/image_raw', Image)
    ts = message_filters.TimeSynchronizer([rgb_sub, dep_sub], 30)

    pub = rospy.Publisher('/camera/rgbd', rgbd, queue_size=30)
    rospy.init_node('Joule', anonymous=True)

    ts.registerCallback(callback)

    rospy.spin()