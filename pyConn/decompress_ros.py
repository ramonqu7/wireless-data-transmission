#!/usr/bin/env python
import blosc
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge


class pyConnDecompress:

    def __init__(self):




'''

def parseData(data):
    data = zlib.decompress(data).split(" ")
    data = [int(i) for i in data]

    # frame = zlib.decompress(data)
    frame = np.asarray(data, dtype=np.uint8).reshape(480, 640)
    d4d = frame
    d4d = np.uint8(frame.astype(float) * 255 / 2 ** 12 - 1)
    d4d = 255 - cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
    return d4d



br = CvBridge()

  #rospy.loginfo(rospy.get_caller_id() + "I heard")
  cv_image = br.imgmsg_to_cv2(data, desired_encoding="passthrough")

'''
