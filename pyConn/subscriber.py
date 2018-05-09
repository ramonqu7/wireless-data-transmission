#!/usr/bin/env python
import time
import cv2
import numpy as np
import rospy
from std_msgs.msg import String
import zlib
from PIL import Image
import StringIO


count = 0
lasttime = 0
f = True # True - rgb, False - Depth
rgb = np.zeros((480*640*3),dtype=np.uint8).reshape(480,640,3)
d4d = np.zeros((480*640*3),dtype=np.uint8).reshape(480,640,3)


def parseData(data):
    #print(len(data))
    data = blosc.unpack_array(data)
    #print(data.shape)
    data = np.dsplit(data,[3])

    #data = np.fromstring(data, dtype = np.uint8).reshape(240,320)
    #color = zoom(np.fromstring(data[0], dtype=np.uint8).reshape(240,320,3), [2,2,1])
    #depth = zoom(np.fromstring(data[1], dtype=np.uint8).reshape(240,320),[2,2])

    color = data[0]
    depth = data[1].reshape(480,640)
    d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
    return np.hstack((color,d4d))

def parseDepth(data):
    depth = zlib.decompress(data)
    depth = np.fromstring(depth, dtype=np.uint8).reshape(480,640)
    d4d = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
    return d4d

def parseRgb(data):
    rgb = Image.open(StringIO.StringIO(zlib.decompress(data)))
    rgb = np.array(rgb).reshape(480,640,3)
    return rgb

def callback(data):
    global count, lasttime,f, rgb, d4d

    if(f):
        #RGB
        f = not f
        rgb = parseRgb(data.data)

    else:
        #Depth
        f = not f
        d4d = parseDepth(data.data)
    cv2.waitKey(1) & 255
    cv2.imshow("RGBD", np.hstack((rgb,d4d)))
    if (int(round(time.time() * 1000)) - lasttime > 10000):
        lasttime = int(round(time.time() * 1000))
        print("Average FPS:" + str(count / 20.0))
        count = 0
    count += 1


def listener():
    global count, lasttime
    print("Start")
    rospy.init_node('Ramon', anonymous=False)
    print("Finish initialize ROS node")
    lasttime = int(round(time.time() * 1000))
    rospy.Subscriber("/RGBD", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()



'''def callbackr(data):
    global rb, gb, bb, db, r,g,b,d
    r = parseData(data.data)
    rb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackg(data):
    global rb, gb, bb, db, r,g,b,d
    g = parseData(data.data)
    gb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackb(data):
    global rb, gb, bb, db, r,g,b,d
    b = parseData(data.data)
    bb = True
    #if(rb and gb and bb and db):
        #show_image()
def callbackd(data):
    global rb, gb, bb, db, r,g,b,d
    d = parseData(data.data)
    d = 255 - cv2.cvtColor(d,cv2.COLOR_GRAY2RGB)
    db = True
    #if(rb and gb and bb and db):
        #show_image()
def show_image():
    global rb, gb, bb, db, r,g,b,d, count, lasttime
    rb = False
    gb = False
    bb = False
    db = False
    cv2.waitKey(1) & 255
    rgb = np.dstack((r,g,b))
    cv2.imshow("RGBD", np.hstack((rgb, d)))
    '''
