#!/usr/bin/env python
import cv2
from openni2_device_init import visionsensor
import numpy as np
from PIL import Image
from io import BytesIO
import time
import zlib


class VideoCamera(object):
    def __init__(self,x = 640, y = 480, fps = 30, rgb_mirror = False,
            depth_mirror = False, rgb = True, depth = True):
        self.device = visionsensor(x = x, y = y, fpd = fps, rgb_mirror = rgb_mirror,
                depth_mirror = depth_mirror, rgb = rgb, depth = depth)
        self.rgb = rgb
        self.depth = depth
        time.sleep(1)


    def __del__(self):
        self.device.stop()

    def get_frame(self, rgb_compress = 75):
        jpeg = ''
        depth = ''
        if self.rgb:
            rgb = self.device.getRgb()
            #img = Image.fromarray(rgb)
            #fpath =BytesIO()
            #img.save(fpath, quality = 75, format = "JPEG")
            #fpath.seek(0)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), rgb_compress]
            ret, jpeg = cv2.imencode('.jpg', rgb, encode_param)
            jpeg = jpeg.tobytes()
        if self.depth:
            depth = zlib.compress(self.device.getDepth2Int8())
        return jpeg, depth
