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

def callback(rgb, dep):
    global pub, bridge, RGB_COMPRESS
    rgbd_msg = Rgbd()
    rgbd_msg.header = dep.header
    rgbd_msg.encoding = rgb.encoding

    try:
        rgb_data = bridge.imgmsg_to_cv2(rgb,"brg8")
    except CvBridgeError as e:
        print(e)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), RGB_COMPRESS]
    ret, rgb_compressed = cv2.imencode('.jpg', rgb_data, encode_param)
    rgb_compressed = rgb_compressed.tobytes()

    try:
        dep_data = bridge.imgmsg_to_cv2(dep,"brg8") #may not be brg8
    except CvBridgeError as e:
        print(e)
    #Trim down to 1d Array
    dep_data = np.hsplit(dep_data,3)[0]
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

    rgb_sub = message_filters.Subscriber('rgb/image_raw', Image)
    dep_sub = message_filters.Subscriber('depth/image_raw', Image)
    ts = message_filters.TimeSynchronizer([rgb_sub, dep_sub], 10)

    pub = rospy.Publisher('/camera/rgbd', Rgbd, queue_size=10)
    rospy.init_node('Joule', anonymous=True)

    ts.registerCallback(callback)

    rospy.spin()