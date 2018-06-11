#!/usr/bin/env python
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
    while True:
        rgb,depth = camera.get_frame()
        yield (b'--frame'+str.encode(str(len(rgb)))+b'f'+str.encode(str(len(depth)))+b'e\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + rgb + depth + b'\r\n\r\n')

#The GET response for camera frames
@app.route('/video_feed')
def rgb_feed():
    return Response(gen(VideoCamera(x = videoX, y = videoY, fps = videoFps, rgb = rgb, depth = depth)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# To retrive the camera info before get the camera frames
@app.route('camera_info')
def camera_info():
    return Response("-X"+str(videoX)+"-Y"+str(videoY),
                        mimetype='text/xml')



if __name__ == '__main__':

    #Global Variables:
    app = Flask(__name__)
    videoX = 640
    videoY = 480
    videoFps = 30
    rgb = True
    depth = True
    ip = ""
    port = random.randint(4999,6000)

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
        if "-rgb" in myargs:
            rgb = True if myargs["-rgb"]=="t" else False
        if "-depth" in myargs:
            depth = True if myargs["-depth"]=="t" else False
    except Exception, e:
        print(e.message)

    if ip == "":
        print("Please Enter IP Address of the local machine")
    else:
        print("Starting the Server on "+ip+':' +str(port))

        app.run(host=ip, port=port, debug=True)
