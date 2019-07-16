https://github.com/jetsonhacks/installROSTX2 Should be working.   For Installing ROS Kinetic
https://github.com/ramonidea/installROSTX2 for install ROS melonic

https://github.com/jetsonhacks/installLibrealsenseTX2.git
This seems an old repo, which did not patch the kernal correctly, so that the jetson tx2 cannot recognize camera as an USB 3.0 device


https://github.com/jetsonhacks/buildLibrealsense2TX

Install pyCuda
https://wiki.tiker.net/PyCuda/Installation/Linux

Install pytorch  
https://gist.github.com/dusty-nv/ef2b372301c00c0a9d3203e42fd83426

Updated: -> https://gist.github.com/ramonidea/0a4e6e53afa4c96204b3f215ad588d7c

Need to fix one issue
https://github.com/pytorch/pytorch/issues/8103

Set up for tensorFlow
https://github.com/NVIDIA-AI-IOT/tf_trt_models#setup

Tensorflow model 
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
`ssd_mobilenet_v1_fpn_coco` or `ssd_resnet_50_fpn_coco`



TensorRT Inference Server
https://github.com/dusty-nv/jetson-inference





Command I ran:
Install ROS + Realsense + Realsense ROS Wrapper

```
cd ~
git clone https://github.com/jetsonhacks/installROSTX2
./installROS.sh -p ros-kinetic-desktop -p ros-kinetic-rgbd-launch -p ros-kinetic-image-transport-plugins
./setupCatkinWorkspace.sh catkin_ws

# Finish installing ROS and setup a catkin space
#START install realsense
cd ~
git clone https://github.com/jetsonhacks/buildLibrealsense2TX

./installLibrealsense.sh
cd ~
git clone https://github.com/jetsonhacks/installRealSense2ROSTX
```



Install Open CV
https://jkjung-avt.github.io/opencv3-on-tx2/
OPen cv install the library into path /usr/local/lib/python2.7/dist-packages
We need to modify the $PYTHONPATH globally to move rearrange the order.


Install pycaffe
https://jkjung-avt.github.io/caffe-on-tx2/


