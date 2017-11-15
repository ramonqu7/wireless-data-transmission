#!/usr/bin/python
import cv2
import numpy as np
from primesense import openni2
from primesense import _openni2 as c_api
from primesense._openni2 import OniSensorType


n = True
openni2.initialize("C:\Program Files\OpenNI-Windows-x86-2.3\Samples\Bin")
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
#depth_stream = dev.create_color_stream()
#depth_stream = dev.create_stream(OniSensorType.ONI_SENSOR_COLOR)
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                                              resolutionX = 640, resolutionY = 480, fps = 30))
#depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
#                                              resolutionX = 640, resolutionY = 480, fps = 30))
while True:
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (1, 480, 640)
    #img.shape = (1,640,720)
    img = np.concatenate((img), axis=0)
    #img = np.swapaxes(img, 0, 2)
    #img = np.swapaxes(img, 0, 1)
    if (n):
        n = False
        print(type(img))
    cv2.imshow("image", img)
    cv2.waitKey(34)
openni2.unload()