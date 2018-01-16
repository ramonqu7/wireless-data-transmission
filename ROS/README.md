# StructureIO Depth Data with ROS (Custom with Python)

## The openi2_device_init.py is the custom class to initialize the openni2 device and get depth, color frames from the device.
``` python
VisionSensor()  # The object for initializing the openni2 Device

- createColor(x=640,y=480,fps = 30) #Create color camera
- createDepth(x=640,y=480,fps=30) # create Depth camera
- sync() #call this function, if using RGBD camera and using both cameras
- getRgb(x = 640,y = 480,fps = 30) # Get RGB numpy array
- getDepth(x = 640, y = 480) # Get Depth numpy Array
- converDepth2Gray() # Convert Depth numpy Array (int16 -> int8) decrease the size of the data
- getRgbd() # append depth data into color frame data
```
