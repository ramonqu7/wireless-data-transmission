#!/usr/bin/env python
import time
import zlib

import cv2
import numpy as np
import rospy
from std_msgs.msg import String

count = 0
lasttime = 0


def parseData(data):
    frame = zlib.decompress(data)
    frame = np.fromstring(frame, dtype=np.uint8).reshape(480, 640, 3)
    d4d = frame
    # d4d = np.uint8(frame.astype(float) * 255 / 2 ** 12 - 1)
    # d4d = 255 - cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
    return d4d


def callback(data):
    global count, lasttime
    # rospy.loginfo(rospy.get_caller_id() + "I heard")

    cv2.waitKey(1) & 255
    cv2.imshow("Depth", parseData(data.data))
    if (int(round(time.time() * 1000)) - lasttime > 30000):
        lasttime = int(round(time.time() * 1000))
        print("Average FPS:" + str(count / 30.0))
        count = 0
    count += 1


def listener():
    global count, lasttime
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=False)
    lasttime = int(round(time.time() * 1000))
    rospy.Subscriber("CameraTest", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
