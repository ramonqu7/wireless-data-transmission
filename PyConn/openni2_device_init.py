import cv2
from primesense import openni2  # , nite2
from primesense import _openni2 as c_api
import numpy as np

class VisionSensor:
    def __init__(self):
        # Linux
        self.dist = '/home/test/Desktop/OpenNI-Linux-x64-2.2/Redist/'
        openni2.initialize(self.dist)
        if (openni2.is_initialized()):
            print("openNI2 initialized")
        else:
            print("openNI2 not initialized")
        ## Register the device
        self.dev = openni2.Device.open_any()

    def createColor(self,x=640,y=480,fps = 30):
        self.rgb_stream = self.dev.create_color_stream()
        self.rgb_stream.set_video_mode(c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,resolutionX = x,
            resolutionY = y,fps = fps))
        self.rgb_stream.set_mirroring_enabled(False)
        self.rgb_stream.start()

    def createDepth(self,x=640,y=480,fps=30):
        self.depth_stream = self.dev.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=x,
                               resolutionY=y,
                               fps=fps))
        self.depth_stream.set_mirroring_enabled(False)
        self.depth_stream.start()

    def sync(self):
        self.dev.set_depth_color_sync_enabled(True)  # synchronize the streams
        ## IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
        self.dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

    def getRgb(self,x = 640,y = 480,fps = 30):
        #Returns numpy 3L ndarray to represent the rgb image.
        self.bgr   = np.fromstring(self.rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(y,x,fps)
        self.rgb   = cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)
        return self.rgb

    def getDepth(self, x = 640, y = 480):
        """dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
             #d4d := depth for dislay, 3L ndarray, dtype=uint8, min=0, max=255    
            Note1: 
                fromstring is faster than asarray or frombuffer
            """
        self.dmap = np.fromstring(self.depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(y, x)
        return self.dmap

    def converDepth2Gray(self):
        self.d4d = np.uint8(self.dmap.astype(float) * 255 / 2 ** 12 - 1)  # Correct the range. Depth images are 12bits
        self.d4d = 255 - cv2.cvtColor(self.d4d, cv2.COLOR_GRAY2RGB)
        return self.d4d

    ##Need to check whether it may work
    def getRgbd(self):
        #4L ndarray , rgb and depth array
        rgb = self.getRgb()
        depth = self.getDepth()
        self.rgbd = []
        for i in range(len(rgb)):
            rgb[i].append(depth[i])
            self.rgbd.append(rgb[i])
        return self.rgbd













