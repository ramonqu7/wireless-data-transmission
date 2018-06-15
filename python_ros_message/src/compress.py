#!/usr/bin/env python
import message_filters
from sensor_msgs.msg import Image
from rgbd_compress.msg import Rgbd
import rospy
import zlib
import numpy as np
from PIL import Image
from io import BytesIO
import cv2



def callback(image, image):
    global pub
'''
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), rgb_compress]
            ret, jpeg = cv2.imencode('.jpg', rgb, encode_param)
            jpeg = jpeg.tobytes()
        if self.depth:
            depth = zlib.compress(self.device.getDepth2Int8())
'''




if __name__ == '__main__':
    rgb_sub = message_filters.Subscriber('rgb/image_raw', Image)
    dep_sub = message_filters.Subscriber('depth/image_raw', Image)
    
    ts = message_filters.TimeSynchronizer([rgb_sub, dep_sub], 10)

    pub = rospy.Publisher('/camera/rgbd', Rgbd, queue_size=10)
    rospy.init_node('Joule', anonymous=True)


    ts.registerCallback(callback)


    rospy.spin()