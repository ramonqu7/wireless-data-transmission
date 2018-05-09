#!/usr/bin/env python
import cv2
import numpy as np
import time
from flask import Flask, render_template, Response

class VideoCamera(object):
    def __init__(self,type):
        self.name = "../pic/"+type+"_"
        self.count = 0
    def __del__(self):
        self.count = 0
    def get_frame(self):
        self.count+=1
        if(self.count > 400):
            self.count = 1
        self.filename = self.name+str(self.count)+".png"
        color = cv2.imread(self.filename)
        ret, jpeg = cv2.imencode('.jpg', color)
        return jpeg.tobytes()#fpath.getvalue()



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame'+str.encode(str(len(frame)))+b'e\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/rgb_feed')
def rgb_feed():
    return Response(gen(VideoCamera('rgb')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/depth_feed')
def depth_feed():
    return Response(gen(VideoCamera('depth')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5151)
