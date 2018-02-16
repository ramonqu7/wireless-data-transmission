# Joule System Set up

Intel Joule 570x:
https://software.intel.com/en-us/intel-joule-getting-started
Has Wifi built-in

## Install OS on the board
* Need to Flash the BIOS first with Intel Flash tool and the updated Intel Joule BIOS, with type C cable connected to the board. [Link to Intel BIOS update](https://software.intel.com/en-us/node/721469)
> Otherwise, it will not auto-boot the OS install program
* IoT website has the setting up tutorials and the ubuntu website has the ubuntu OS install tutorial
  - [Install Ubuntu Tutorial Video](https://software.intel.com/en-us/videos/installing-ubuntu-on-the-intel-joule-compute-module)
    - With Ubuntu, the Joule is easily getting hot and force the board to shut down. Be aware of the risk of losing files.
  - Also recommend to install light-weight OS like [Lubuntu](https://docs.lubuntu.net/)
  - Ubuntu has a Core 16 which indicates to the embedded sys, but it requires the Internet all the times. 
- You can also install other systems. [Check this website.](https://software.intel.com/en-us/choosing-among-oses)
> But we are using ROS, so it would be the best to install Ubuntu system.
* Things about Intel Joule Board:
  - It has wifi and bluetooth module on board which may be convenient feature for wireless transmission. The wifi supports wifi-direct.
  - The type -C only for flash the BIOS. We need a USB hub for the USB port.(keyboard, mouse and maybe flash drive) The micro-USB can be connected to the host machine and use putty or other serial monitor to read the debug mode serial output. (The host machine needs to install driver)
  
  
```
sudo apt-get update
sudo apt-get install git python-pip python3-pip
sudo apt-get -qq install -y libsm6 libxext6 && pip install -q -U opencv-python
pip install -U numpy primesense pillow


```
  
  
  
```diff
- The following installation of the ROS is actually not required for the final product, 
- but I tested with ROS wireless transmission as well. (Only test purpose, not recommended to install)
```

------
The following is not required any more for the final product.
  ## Install ROS and other necessary Software on ubuntu

Install the Ros-Base
> The Joule may not need other tools for wireless data transmission purpose, if we need to do more post-processing before transmitting, you may install individual package or the  ros-kinetic-desktop version
The ros-kinetic-desktop-full version may take too much disk space

```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update && sudo apt-get install ros-kinetic-ros-base
```
Initialize Rosdep
```
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
Dependencies for building packages
```
sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential git python-pip python-catkin-tools python-wstool
sudo pip install -U pip
```
## Development Environment Set up
```
$ mkdir my-workspace && cd my-workspace
$ wstool init src
$ catkin init
$ catkin config --extend /opt/ros/kinetic

```
