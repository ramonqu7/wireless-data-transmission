import cv2
from primesense import openni2
from primesense import _openni2 as c_api
import numpy as np

class visionsensor:
    def __init__(self):
        # Linux
        self.dist = '/home/test/ws/src/pyRamon/pyConn/OpenNI-Linux-x64-2.3/Redist/'
        openni2.initialize(self.dist)
        if (openni2.is_initialized()):
            print("openNI2 initialized")
        else:
            print("openNI2 not initialized")
        ## Register the device
        self.dev = openni2.Device.open_any()

    #Start the Color Camera
    def startColor(self):
            self.rgb_stream.start()
            print("RGB camera start")

    #Start the Depth Camera
    def startDepth(self):
            self.depth_stream.start()
            print('Depth camera start')

    #Stop the Depth Camera
    def stopDepth(self):
        self.device.depth_stream.stop()
        print("Stop Depth Camera")

    #Stop the Color Camera
    def stopColor(self):
        self.device.rgb_stream.stop()
        print("Stop RGB Camera")

    #Initialize color camera (default 640 * 480 * 30fps)
    def createColor(self,x=640,y=480,fps = 30):
        self.rgb_stream = self.dev.create_color_stream()
        self.rgb_stream.set_video_mode(c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,resolutionX = x,
            resolutionY = y,fps = fps))
        self.rgb_stream.set_mirroring_enabled(False)
        print("Intialize the Color Camera")

    #Initialize the Depth camera (default 640*480*30fps)
    def createDepth(self,x=640,y=480,fps=30):
        self.depth_stream = self.dev.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=x,
                               resolutionY=y,
                               fps=fps))
        self.depth_stream.set_mirroring_enabled(False)
        print("Initialize the Depth Camera")


    #Enable the depth and color sync (un after initalized both cameras, before running them)
    def sync(self):
        self.dev.set_depth_color_sync_enabled(True)  # synchronize the streams
        ## IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
        self.dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

    #Return / Initalize self.rgb as the numpy array (uint8 3L 640 * 480 * 3 * uint8)
    def getRgb(self,x = 640,y = 480):
        #Returns numpy 3L ndarray to represent the rgb image.
        self.bgr   = np.fromstring(self.rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(y,x,3)
        self.rgb   = cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)
        return self.rgb

    #Return self.dmap as the numpy array (1L uint16, 0 - 2**12-1)
    def getDepth(self, x = 640, y = 480):
        """dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
             #d4d := depth for dislay, 1L ndarray, dtype=uint8, min=0, max=255
            Note1:
                fromstring is faster than asarray or frombuffer
            """
        self.dmap = np.fromstring(self.depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(y, x)
        return self.dmap

    # Return the depth as numpy array (1L uint8) (reshape the range of the value 0 - 255)
    def getDepth2Int8(self, x = 640, y = 480):
        self.dmap = np.fromstring(self.depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(y, x)
        self.d4d = np.uint8(self.dmap.astype(float) * 255 / 2 ** 12 - 1)  # Correct the range. Depth images are 12bits
        return self.d4d

    #Return Depth2Gray image which can be show with cv2
    def getDepth2Gray(self):
        self.d4d = 255 - cv2.cvtColor(self.d4d, cv2.COLOR_GRAY2RGB)
        return self.d4d

    ##Need to check whether it may work
    def getRgbd(self, x = 640, y = 480):
        #4L ndarray , rgb and depth array
        rgb = self.getRgb(x,y)
        depth = self.getDepth2Int8(x,y)
        self.rgbd = []
        for i in range(len(rgb)):
            rgb[i].append(depth[i])
            self.rgbd.append(rgb[i])
        return self.rgbd
