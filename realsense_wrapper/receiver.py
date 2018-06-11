try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import numpy as np
import PIL.Image
import StringIO
import cv2
from io import BytesIO
import time
import zlib
import rospy
import json
from sensor_msgs.msg import CompressedImage,CameraInfo, Image
from std_msgs.msg import String, Header
from cv_bridge import CvBridge, CvBridgeError
from sys import argv

def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
def detect_faces(f_cascade, colored_img, scaleFactor = 1.1):
    img_copy = np.copy(colored_img)
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    #let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    #go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return img_copy
lbp_face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#To parse the command line arguments
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def getFrame(response):
    rgbData = b''
    depthData = b''
    while 1:
        temp = response.read(4096)
        a = temp.find(b'e\r\nContent-Type: image/jpeg\r\n\r\n')
        b = temp.find(b'--frame')
        if(a==-1):
            rgbData += temp
        else:
            head = temp[b+7:a]
            rgb = head.find(b'f')
            depth = head[rgb+1:]
            rgb = head[:rgb]
            rgbData = temp[a+31:]
            break
    num = int(rgb)
    left = num - (4096-a-31)
    rgbData += response.read(left)
    depthData = response.read(int(depth))
    return rgbData, zlib.decompress(depthData)

def retriveCameraInfo(ip, port):
    global videoX,videoY,D,K,R,P
    info = urlopen("http://"+ip+':'+port+'/camera_info')
    result = str(info.read(1024))
    result = json.loads(result)
    videoX = result["X"]
    videoY = result["Y"]
    D = result["coeffs"]
    K = [result["fx"],0,result["ppx"],
        0,result["fy"],result["ppy"],
        0,0,1]
    R = result["rot"]

    info_msg = CameraInfo()
    info_msg.height = videoY
    info_msg.width = videoX
    info_msg.header.stamp = rospy.Time.now()
    info_msg.D = D
    info_msg.K = K
    info_msg.R = R

    return info_msg


if __name__ == '__main__':
    #Global Variables

    ip = ''
    port = ''
    videoX = 640
    videoY = 360
    videoFps = 30
    rgb = True
    depth = True
    D = []
    K = []
    R = []
    P = []



    myargs = getopts(argv)
    try:
        if "-ip" in myargs:
            ip = myargs["-ip"]
        if "-port" in myargs:
            port = myargs["-port"]
    except Exception:
        print(e.message)

    if ip == "" or port == '':
        print("Please Enter IP Address of the local machine")
    else:
        print("Remote Joule is set to "+ip+':' +str(port))
        print("Init ROS")
        #rgb_pub = rospy.Publisher("/Camera/rgb",CompressedImage,queue_size=10)
        #print("/Camera/rgb is published, (CompressedImage)")
        #depth_pub = rospy.Publisher("/Camera/depth",Image,queue_size=10)
        #print("/Camera/depth is published, (Image)")
        #camera_info = rospy.Publisher("/Camera/camera_info",CameraInfo,queue_size=10)
        #print("/Camera/camera_info is published, (camera_info)")
        #rospy.init_node("Joule", anonymous=False)
        #info_msg = retriveCameraInfo(ip,port)
        print("Finish the camera Info")
        #while not rospy.is_shutdown():
        while 1:
            '''
            bridge = CvBridge()

            #TODO: Need to add other parameters for the message
            if camera_info.get_num_connections()>0 :
                camera_info.publish(info_msg)
            if depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
                video = urlopen("http://"+ip+":"+port+"/video_feed")
                #TODO:Add exception on this command
                while depth_pub.get_num_connections() > 0 or rgb_pub.get_num_connections() > 0:
                    rgb,depth = getFrame(video)
                    #rgb = np.asarray(PIL.Image.open(BytesIO(rgb)))
                    #faces_detected_img = detect_faces(lbp_face_cascade, rgb)

                    rgb_msg = CompressedImage()
                    rgb_msg.header.stamp = rospy.Time.now()
                    rgb_msg.format = "jpeg"
                    rgb_msg.data = rgb
                    # Publish new image
                    rgb_pub.publish(rgb_msg)


                    depth = np.fromstring(depth,dtype=np.uint8).reshape(480,videoX)

                    #depth = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
                    #cv2.imshow('rgbd', np.hstack((convertToRGB(faces_detected_img),depth)))
                    #if cv2.waitKey(1) & 0xFF == ord('q'):
                    #    break


                    #try:
                    #    depth_pub.publish(bridge.cv2_to_imgmsg(depth, "8UC1"))
                    #except CvBridgeError as e:
                    #    print(e)
                video.close()


'''
            video = urlopen("http://"+ip+":"+port+"/video_feed")

            lasttime = int(round((time.time()*1000)))
            count = 0.0
            while 1:
                rgb,depth = getFrame(video)
                rgb = zlib.decompress(rgb)
                rgb = np.asarray(PIL.Image.open(StringIO.StringIO(rgb)))
                #rgb = np.asarray(PIL.Image.open(BytesIO(rgb)))
                #rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)

                if(int(round((time.time()*1000))) - lasttime > 10000):
                    lasttime = int(round((time.time()*1000)))
                    print("Average FPS:"+str(count / 10.0))
                    count = 0.0
                count +=1


                faces_detected_img = detect_faces(lbp_face_cascade, rgb)
                faces_detected_img = (convertToRGB(faces_detected_img))

                depth = np.fromstring(depth,dtype=np.uint8).reshape(480,videoX)

                depth = 255 - cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
                cv2.namedWindow('PRL', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("PRL", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FREERATIO)
                cv2.imshow('PRL',np.hstack((faces_detected_img, depth)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            video.close()
