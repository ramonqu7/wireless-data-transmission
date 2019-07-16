# **Wireless Perception Module (WiPer V2.0)** - Build From Scratch Tutorial (In Progress)

## Yiren (Ramon) Qu, Rosario Scalise

![CSE](img/prl.PNG) ![CSE](img/cse.PNG)

![ADA](img/intro.jpg)

---

# Table of Contents

1.  [What you'll need](#org11f013c)
2.  [Mechanical](#org437c511)
    1.  [Printing the 3D files](#orgf55114f)
    2.  [Mounting the enclosure to the robot arm](#org37ac3e7)
    3.  [Fitting the hardware to the 3D enclosure](#org6f79684)
3.  [Electrical](#org4b2b1a1)
    1.  [Recommended power source](#org7981dc9)
    2.  [Fabricating the cables](#org4e38be8)
    3.  [Connecting the cables](#org54e2305)
    4.  [Cable summary](#orgdba8e15)
4.  [Software](#org84be803)
    1.  [Installing the OS to the Joule](#orgcbfb208)
    2.  [Installing Required Libraries](#org4290339)
5.  [Recommended Networking Configuration](#orgea01b4a)
    1.  [Client-side (off-board computing) Networking](#org06cd64d)
    2.  [Server-side (end-effector computing) Networking](#orgc67814a)
    3.  [ROS](#orge867589)
6.  [Running](#orgdd11d53)




# <a id="org11f013c">What you'll need </a>
> See [Appendix](orgdrr23431) for an itemized list with purchase links (updated as of June 2018).
1.  Jetson Nano Development Board


2.  Intel RealSense D415 or D435 RGBD Camera (or Openni2 support RGBD cameras)

    2.1 USB type C to A 3.0 cable

    > You may use the cable included with the Joule, or order a shorter one.

![Intel RealSense](img/realsense.png)

3.  3D Printed Parts
    > Models and printed object can be found in the [3D File section](#orgf55114f)

4.  Pololu 5V Step Down. (Voltage Regulator D24V22F12)

5.  Screws:

6. Flat Flex, Ribbon Jumper Cables (20 pins 4.000" (50.80mm)) Molex, LLC 0152670357

![pinConnector](./img/pin_connector.jpg)

7. DC jack for Nano power source (you can "borrow" one from most standard wall-wart style adapters).

![DC Jack](./img/dc-jack.jpg)

8. Optional based upon resources, but we used the Kinova Jaco 7-DOF manipulator (you could also use your own robot and modify the 'cuff mount')

9. Wi-Fi Router. We are using TP Link AC1900.
![](./img/wifi-router.jpg)



# 🔧 <a id="org437c511">Mechanical</a>

## <a id="orgf55114f">Printing the 3D files</a>

-   Here are the [3D Print-ready files](./3d_model/) for the Intel Joule housing box and mount with the end-effector.

> Note: The incline top is to allow for mounting the camera further back and altering its view angle.

![Mount cuff connector](./img/cuff_link.PNG)

[Mount cuff connector](./3d_model/ring_final.STL)

Assembly look with incline case top:


### Print Settings

- We used Solidworks to design and test assembly fit for each part.
- We printed the model with [Ultimaker 2+](https://ultimaker.com/) and [Creator Pro](http://www.flashforge.com/creator-pro-3d-printer/). The settings used are listed below:
    - Layer height: 0.1 mm
    - Infill Percentage: 50%
    - Temperature: 225°C

> - Alternatively, [Shapeways](www.shapeways.com) supplies high quality 3D print services.

- The final printed models:

![Mount cuff connector](./img/connector_printed.jpg)

Mount cuff connector


Jerson Nano enclosure body


Intel Joule box flat enclosure top


Intel Joule box incline enclosure top



## <a id="org37ac3e7">Mounting the enclosure to the robot arm</a>

![mount step 1](./img/mount_1_1.jpg)

![mount step 1](./img/mount_1_ink.jpg)

1. Connect the enclosure body [#3.1] and the end-effector cuff connector [#3.4] with 2X screws [#5.3]

![mount step 2](./img/mount_2_ink.jpg)

2. Unscrew the Kinova Jaco's last joint's top three screws. And directly secure the assembled parts (enclosure body + cuff connector) to the arm with 3X screw [#5.3]





## <a id="org6f79684">Fitting the hardware to the 3D enclosure</a>

### Insert the Jetson Nano into the enclosure

![mount step 3](./img/mount_3_ink.jpg)

-  Secure the Jetson Nano board [#1] into the enclosure with 4 X Screws [#5.1].

> Please make sure the two wifi antenna would not touch each other and able to be fit in the enclosure.

### Attach camera to the enclosure

Camera Mount 1

![Picture of attaching camera position 1](./img/flat_mount.jpg)

Camera Mount 2

![Picture of attaching camera position 2](./img/incline_mount.jpg)

1. Install incline camera mount:

    5.1 Secure the incline enclosure top with 4X screws [#5.2]

    5.2 Mount the camera on the enclosure with 1X screws [#5.4].

    > Make sure the camera is securely mounted with the enclosure, which would not resulting much vibration when the end effector's moving

    5.3 Connect camera and the Intel Joule with USB type C to A 3.0 cable [#2.1]


# ⚡️ <a id="org4b2b1a1">Electrical</a>




## 🔌 <a id="org7981dc9">Recommended power source</a>

-   Intel Joule with Intel RealSense D435 running requires ≥ 1.5A @ 12V
> ❗️Jetson Nano only requires XXA @ 5V to boot.
-   Kinova Mico Joint 6 supplies max 3A @ 24V
-   Inside the hand, there is limited space to store the power conversion circuit. We use buck convertor from Pololu [#4] to convert the power from Kinova arm to supply Jetson Nano.


## <a id="org4e38be8">Fabricating the cables</a>

![schematic diagram](img/elec.PNG)

-  The electronic schematic diagram of the power system.


## <a id="org54e2305">Connecting the cables</a>

-   The final connected cable

![final connected cable image1](img/connected_1.PNG)

![final connected cable image2](img/connected_2.jpg)

 We drilled a hole from the hand for the DC jack to go through.

 ![dcjack Hole](img/dcjack_hole_1.jpg)


-  Plugging into board

![plugging into board](img/plug_board.jpg)


<a id="orgdba8e15"></a>

## Cable summary

![Picture with Nano and all the things plugged into it](img/plug_all.jpg)

<a id="org84be803"></a>

# Software

<a id="orgcbfb208"></a>

## Installing the OS and software to the Nano

- Please check [this post](./Jetson-Nano-Setup.md) to install the OS and software onto the Jetson Nano


<a id="org4290339"></a>

## Installing Required Libraries

- [ROS required packages (with minor modifications)](https://github.com/ramonidea/prl_wireless_perception.git)

    - [ROS Image Transport Plugins](https://github.com/ros-perception/image_transport_plugins.git)

    We used Compressed Image Transport Plugins to compressed the RGB Images.

    - [ROS Image Pipeline](https://github.com/ros-perception/image_pipeline.git)

    We used one function `point_cloud_xyzrgb` inside the `depth_image_proc` to reconstruct the point cloud data from RGB and Depth images.

    > And their dependency packages `image_common` and `image_geometry`

    - [RGBD_Message](https://github.com/ramonidea/prl_wireless_perception/tree/master/rgbd_message)

        This is a custom package trying to solve the problem that depth and color images are not arriving at the same time. This send a message with serialized rgb and depth image data. And we used JPEG lossy compression on Color and lossless compression on Depth.

- [Realsense Camera Driver](https://github.com/IntelRealSense/librealsense)

    Please follow the [README document](https://github.com/IntelRealSense/librealsense/blob/master/readme.md) to install the driver.

- [RealSense Camera ROS Wrapper](https://github.com/intel-ros/realsense)

    Please build this after installing the driver.

## Networking Diagram

![Optiuon 1](./img/option_1.PNG)

Option 1

This option is mainly rely on Python codec and ROS realsense wrapper. It compresses RGB and Depth into one serialized array topic with custom message type: `/camera/rgbd`. And the client side run the decompress methods to separate the one topic into two topics: `/camera/color/decompressed` and `/camera/depth/decompressed`, or it may use the decompression pacakge, which you can call the decompress function in your client side and decompress into two frames without republishing.



![Option 2](./img/option_2.PNG)

Option 2

This option is mainly rely on C++ and ROS realsense wrapper. It compresses RGB and Depth image separately into two topics: `/camera/color/image_raw/compressed` and `/camera/depth/image_raw/compressedDepth`. And the client side may use `Message_filter` to synchronize those two topics.

<a id="orgea01b4a"></a>

# Recommended Networking Configuration

![Networking](img/networking.PNG)

<a id="org06cd64d"></a>

## Client-side (off-board computing) Networking

-   We are currently using [#10] TP-Link Router.
-   We set the static IP addresses for both the client side and the server side.

We will run the _**roscore**_ on the client side.

<a id="orgc67814a"></a>

## Server-side (end-effector computing) Networking

-   Because we run the rerscore on the client side, please use command to set `ROS_MASTER_URI` and `ROS_IP` on each machine.


<a id="orge867589"></a>

## ROS

-   use command `ifconfig` to retrieve the IP address from your workstation.

> The ip addresses should be always the same, because we save the ip address in the router setting from the last step.

-  Please make sure the Joule's `ROS_MASTER_URI` has been set to that ip address. And set the `ROS_IP` correctly.


> As an example, if your workstation (ip address `192.168.1.10`) running `roscore` has a wireless adapter IP of `192.168.1.12`, then make sure your terminal running the ROS environment has its `ROS_MASTER_URI` pointed to the workstation like so: `export ROS_MASTER_URI=http://192.168.1.10:11311` and set joule ip address with command: `export ROS_IP=192.168.1.12`


<a id="orgdd11d53"></a>

# Running

-   Please refer to the ADA-Joule demo described in this [document](Intel-Joule-ADA-Perception-Demo.md).

<a id="orgdrr23431"></a>

# Appendix

<a id="orgdr23442"></a>

## Bill of Materials

|                   Part Name                   | Num of Part |    Price   | Purchase Link |
|:---------------------------------------------:|:-----------:|:----------:|:----------:|
|                  Kinova Robot                 |      1      | Pricey |  https://www.kinovarobotics.com/en/products/robotic-arm-series    |
|         Jetson Nano Developer Kit        |      1      |   $99.00  |   https://developer.nvidia.com/embedded/jetson-nano-developer-kit   |
|             Intel Real Sense D435             |      1      |   $179.00  |  https://click.intel.com/intelr-realsensetm-depth-camera-d435.html    |
|             3D PLA 1.75mm Filement            |  1kg Spool  |   $20.00   |  https://www.amazon.com/HATCHBOX-3D-Filament-Dimensional-Accuracy/dp/B00J0ECR5I/ref=sr_1_2?ie=UTF8&qid=1530140364&sr=8-2&keywords=pla%2B1.75mm%2Bblack&th=1    |
|           Intel Joule Box (3d print)          |      1      |    Free    |  N/A    |
|Wrist Mount(3d print)|1|Free|N/A|
|M3 X 10 Screws| 6 |---| https://www.mcmaster.com/94500a223 |
|                   M6 X 10 Screws                  |     1     |    ---        | https://www.mcmaster.com/94500a314 |
|                   M3 X 6 Screws                   |     5     |     ---       |   https://www.mcmaster.com/91294a126   |
|                   M3 Washer       |   2 (optional) for the camera  |    ---    | https://www.mcmaster.com/90965a130 |
|                   M2 X 8 Screws                   |     4     |    ---     |  https://www.mcmaster.com/91294a005    |
| Pololu 12v 2.2A step down regulator D22V22F12 |      1      |    $9.95        |  https://www.pololu.com/product/2855    |
| DC Barrel Jack Connector |      1      |    $2.13        |  https://www.digikey.com/product-detail/en/tensility-international-corp/CA-2189/CP-2189-ND/568580    |
| Molex 20-conductor Ribbon Cable |      1      |    $2.64        |  https://www.digikey.com/product-detail/en/molex-llc/0152670369/WM10552-ND/4427241    |
| Wi-Fi Router. We are using TP Link AC1900     |      1      |   $89.99         |  http://a.co/hMIWrfC   |
