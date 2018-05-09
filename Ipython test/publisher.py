#!/usr/bin/env python
import cv2
import numpy as np
import time
import zlib
from flask import Flask, render_template, Response

class VideoCamera(object):
    def __init__(self):
        self.name = "../pic/"
        self.count = 0
    def __del__(self):
        self.count = 0
    def get_frame(self):
        self.count+=1
        if(self.count > 400):
            self.count = 1
        self.filename = self.name+"rgb_"+str(self.count)+".png"
        color = cv2.imread(self.filename)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
        ret, jpeg = cv2.imencode('.jpg', color,encode_param)
        
        self.filename = self.name+"depth_"+str(self.count)+".png"
        depth = zlib.compress(cv2.imread(self.filename))
        

        return jpeg.tobytes(), depth



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        rgb,depth = camera.get_frame()


        yield (b'--frame'+str.encode(str(len(rgb)))+b'f'+str.encode(str(len(depth)))+b'e\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +rgb+depth + b'\r\n\r\n')

@app.route('/video_feed')
def rgb_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5000)
