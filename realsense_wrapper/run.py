#!/usr/bin/env python3
#
# This scipt host Flask server on the local Joule machine and set up multiple
# data streams for camera frames, camera info
#
# Also, it allows to set the basic settings of the camera, like resolution,
# fps, .....
#
# Usage:
# python run.py
# Argument options:
# -ip {local IP adress}
# -x {resolution X} -y {resolution Y} -fps {fps}
# -rgb {t/f open/close rgb camera} -depth {t/f open/close depth camera}
# TODO:
# Add camera callebration settings
# Make python to read Joule IP Adress

import random
from sys import argv
from flask import Flask, render_template, Response
from camera import VideoCamera
import pyrealsense2 as rs
import json
import numpy as np
import zlib
import PIL.Image


import cv2

app = Flask(__name__)

#Default values
videoX = 640
videoY = 360
videoFps = 30
ip = ""
port = random.randint(4999,6000)

intrinsics = ""
extrinsics = ""

#To parse the command line arguments
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

#Host a normal website to show the instructions
@app.route('/')
def index():

    return render_template('index.html')

#Continuous return camera frame
def gen(camera):
    camera.start_camera()
    while True:

        rgb,depth = camera.get_frame()
        rgb = zlib.compress(rgb)
        yield (b'--frame'+str.encode(str(len(rgb)))+b'f'+str.encode(str(len(depth)))+b'e\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + rgb + depth + b'\r\n\r\n')

#The GET response for camera frames
@app.route('/video_feed')
def rgb_feed():
    return Response(gen(VideoCamera(x = videoX, y = videoY, fps = videoFps)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def get(camera):
    camera.start_camera()
    intrinsics_d, extrinsics_d, intrinsics_c, extrinsics_c = camera.get_camera_info()
    result = {
        "X":videoX,
        "Y":videoY,
        "ppx": intrinsics_d.ppx,
        "ppy": intrinsics_d.ppy,
        "fx":intrinsics_d.fx,
        "fy":intrinsics_d.fy,
        "coeffs":intrinsics_d.coeffs,
        "rot":extrinsics_d.rotation,
        "tra":extrinsics_d.translation
    }


    return(json.dumps(result))

# To retrive the camera info before get the camera frames
@app.route('/camera_info')
def camera_info():
    return Response(get(VideoCamera(x = videoX, y = videoY, fps = videoFps)),
                        mimetype='text/xml')

myargs = getopts(argv)
try:
    if "-ip" in myargs:
        ip = myargs["-ip"]
    if "-port" in myargs:
        port = int(myargs["-port"])
    if "-x" in myargs:
        videoX = int(myargs["-x"])
    if "-y" in myargs:
        videoY = int(myargs["-y"])
    if "-fps" in myargs:
        videoFps = int(myargs["-fps"])
except e:
    print(e.message)

if ip == "":
    print('\x1b[1;37;43m'+"Please Enter IP Address of the local machine" +"\x1b[0m")
else:
    print('\x1b[7;37;41m'+"Starting the Server on "+ip+':' +str(port)+"\x1b[0m")

    print("Test the camera Connection")
    get(VideoCamera(x = videoX, y = videoY, fps = videoFps))


    app.run(host=ip, port=port, debug=False)
