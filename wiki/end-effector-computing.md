# End-effector Computing

![ADA](img/intro.jpg)

---

# Table of Contents

1.  [Notes for writing:](#org4a85d46)
2.  [What you'll need](#org11f013c)
3.  [Mechanical](#org437c511)
    1.  [Printing the 3D files](#orgf55114f)
    2.  [Mounting the enclosure to the robot arm](#org37ac3e7)
    3.  [Fitting the hardware to the 3D enclosure](#org6f79684)
    4.  [Thermal mitigation](#org3c07fc7)
4.  [Electrical](#org4b2b1a1)
    1.  [Recommended power source](#org7981dc9)
    2.  [Fabricating the cables](#org4e38be8)
    3.  [Connecting the cables](#org54e2305)
    4.  [Cable summary](#orgdba8e15)
5.  [Software](#org84be803)
    1.  [Installing the OS to the Joule](#orgcbfb208)
    2.  [Installing Required Libraries](#org4290339)
    3.  [Installing our Wireless Data Transmission Repo](#org9426616)
6.  [Recommended Networking Configuration](#orgea01b4a)
    1.  [Client-side (off-board computing) Networking](#org06cd64d)
    2.  [Server-side (end-effector computing) Networking](#orgc67814a)
    3.  [ROS](#orge867589)
7.  [Running](#orgdd11d53)


<a id="org4a85d46"></a>

# Notes for writing:

-   We might be able to call this work 'End-effector Computing'
-   The first time you refer to parts like 'buck converter', use number next to the part like:
    -   "Solder the Buck Converter [#6] by to the leads from the DC power Jack [#8]".
    -   These part numbers should be the same as in the "What you'll need" section and in the BOM


<a id="org11f013c"></a>

# What you'll need

1.  Intel Joule 570X Developer Kit (or comparable board)

![Intel Joule](img/joule.jpg)

2.  Intel RealSense D415 or D435 RGBD Camera (or openni2 support RGBD cameras)

![Intel RealSense](img/realsense.png)

3.  3D Printed Parts 
    > Model and printed object will be shown in [3D File section](#orgf55114f)

    3.1 Intel Joule enclosure body

    3.2 Intel Joule Box Flat enclosure Top

    3.3 Intel Joule Box Incline enclosure Top

    3.4 Mount cuff connector
4.  Pololu 12V, 2.2A Step Down. (Voltage Regulator D24V22F12)
5.  Optionally, but best for this application Kinova Mico (you could use your own robot and modify the 'cuff mount')

[Here's a detailed Bill of Materials](#orgdr23442) with pricing (as of June 2018) and links to distributors.



<a id="org437c511"></a>

# Mechanical


<a id="orgf55114f"></a>

## Printing the 3D files

-   Here is the [3D Print-ready files](./3d_model/) for the Intel Joule housing box and mount with the End-Effector.

![Intel Joule enclosure body](./3d_model/enclosure_final.STL)

Intel Joule enclosure body

![Intel Joule Box Flat enclosure Top](./3d_model/Top_regular.STL)

Intel Joule Box Flat enclosure Top 

![Intel Joule Box Incline enclosure Top ]()

Intel Joule Box Incline enclosure Top 

![Mount cuff connector](./3d_model/ring_final.STL)

Mount cuff connector

![Assembly]()

Assembly

- I used Solidworks designed each part and test the final assembled parts.
- I printed the model with [Ultimaker 2+](https://ultimaker.com/) and [Creator Pro](http://www.flashforge.com/creator-pro-3d-printer/) and settings are listed below:
    - Layer height: 0.1 mm
    - Infill Percentage: 50%
    - Temperature: 225°C

-   Alternatively, Shapeways supplies high quality 3D print services. .....Price is about.....

- The final printed model:

![Finish Model]()

Finish Model


<a id="org37ac3e7"></a>

## Mounting the enclosure to the robot arm

![mount step 1]()

1. Connect the enclosure body [#3.1] and the end effector cuff connector [#3.4] with 2 X Screw [#]

![mount step 2]()

2. Unscrew the Kinova Mico last joint's three screws, which are the three screws shoing in the image. 

![mount step 3]()

3. Direct securely screw the assembled parts(enclosure body + cuff connector) to the arm with screw [#]

![mount step 4]()

4. Secure the Intel Joule board [#1] into the enclosure with 4 X Screws [#].

> Please make sure the two wifi antenna would not touch each other and able to be fit in the enclosure.





<a id="org6f79684"></a>

## Fitting the hardware to the 3D enclosure

-   Picture of how to insert the Joule into the enclosure
-   Picture of attaching camera


<a id="org3c07fc7"></a>

## Thermal mitigation

-   Picture of mounting the cooler


<a id="org4b2b1a1"></a>

# Electrical


<a id="org7981dc9"></a>

## Recommended power source

-   Intel Joule with Intel RealSense running requires at least 1.5A with 12V
> Intel joule only requires about 0.6A with 12V to boot up.
-   Kinova Mico Joint 6 supplies max 3A with 24V
-   Inside the hand, there is limited space to store the power conversion circuit. We use buck convertor from Pololu [#4] to convert the power from Kinova arm to supply intel Joule. 


<a id="org4e38be8"></a>

## Fabricating the cables

![schematic diagram]()

-  The electronic schematic diagram of the power system. 

-   Steps to solder the connections


<a id="org54e2305"></a>

## Connecting the cables

![Kinova side]()

-   Show Kinova side with pictures

![plugging into board]()

-   Show plugging into board


<a id="orgdba8e15"></a>

## Cable summary

-   Show picture with Joule and all the things plugged into it


<a id="org84be803"></a>

# Software


<a id="orgcbfb208"></a>

## Installing the OS to the Joule

- Please check [this post](./Intel-Joule-Setup.md) to install the OS onto the Intel Joule.
- In my project, I used Lubuntu (Ubuntu/Linux core 16.03 LTS) with ROS-Desktop version installed. 


<a id="org4290339"></a>

## Installing Required Libraries

- [ROS Image Transport Plugins](https://github.com/ros-perception/image_transport_plugins.git)

We used Compressed Image Transport Plugins to compressed the RGB Images. 

- [ROS Image Pipeline](https://github.com/ros-perception/image_pipeline.git)

We used one function `point_cloud_xyzrgb` inside the `depth_image_proc` to reconstruct the point cloud data from RGB and Depth images.

- [Realsense Camera Driver](https://github.com/IntelRealSense/librealsense)

Please follow the [README document](https://github.com/IntelRealSense/librealsense/blob/master/readme.md) to install the driver.

- [RealSense Camera ROS Wrapper](https://github.com/intel-ros/realsense)

Please build this after installing the driver.

> If you are using Intel Realsense R435, you may need to change the parameter.
>......The code to do that.




<a id="org9426616"></a>

## Installing our Wireless Data Transmission Repo


<a id="orgea01b4a"></a>

# Recommended Networking Configuration


<a id="org06cd64d"></a>

## Client-side (off-board computing) Networking

-   Show router and configuration page with settings we are using


<a id="orgc67814a"></a>

## Server-side (end-effector computing) Networking

-   Similarly, show how this is configured (if anything special)


<a id="orge867589"></a>

## ROS

-   Briefly mention what needs to be set for ROS to be able to see the networked devices correctly


<a id="orgdd11d53"></a>

# Running

-   Please refer to the README in the accompanying repo [here] for instructions on running the system.


<a id="orgdrr23431"></a>

# Appendix

<a id="orgdr23442"></a>

## Bill of Material
-   Will be a table
-   Must include everything including screws from McMaster, etc.