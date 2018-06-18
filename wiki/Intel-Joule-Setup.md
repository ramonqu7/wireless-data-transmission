## Steps to set up Intel Joule

### **Flash BIOS** _IMPORTANT_
* Need to Flash the BIOS first with Intel Flash tool and the updated Intel Joule BIOS, with type C cable connected to the board. Please check the [online steps](https://software.intel.com/en-us/flashing-the-bios-on-joule) to complete BIOS update.
> Otherwise, it will not auto-boot the OS installer

### Install Operating System on the board
> But if you are going to use ROS with Joule, it would be the best to install Ubuntu/Linux based system.
There are some options:
- **IoT targeted System**
  - Windows IoT
    - Windows discontinue support Intel Joule. But our lab has one Joule installed with Windows IoT.
  - Ubuntu Core
    - [Tutorial to install Ubuntu Core on Intel Joule](https://developer.ubuntu.com/core/get-started/intel-joule)
    - Configure the platform with Ubuntu Core to run snaps.
    

- **Normal Ubuntu/Linux System**
  - Ubuntu
    - [Online video tutorial](https://software.intel.com/en-us/videos/installing-ubuntu-on-the-intel-joule-compute-module)
    > If installing Ubuntu full system on the embedded storage, there will be limited space to run ROS or other programs. I would recommend to install Ubuntu System on the MicroSD card and boot the system from microSD.
    - If running Ubuntu with ROS both on the embedded storage, the space would be limited and the Joule could be easily getting hot and force the board to shut down. Be aware of the risk of losing files. 
    > This issue has been solved by installing a active fan-heatsink module on board. [Here is the purchase link](https://store.gumstix.com/fansink-intel.html)
  - [Lubuntu]((https://docs.lubuntu.net/))
    - Another option to install on lite version of Ubuntu-based system on embedded storage. This would be left more space than before. And we are able to install ROS-base.

### Install essential packages
  
```
sudo apt-get update
sudo apt-get install git python3-pip
sudo apt-get install -y libsm6 libxext6 && pip3 install -U opencv-python numpy 
# sudo apt-get install primesense pillow #If you need to use Openni2 cameras

#The realsense lib wrapper is for python3
#Need to follow the instruction here to set up the machine and install python wrapper
# https://github.com/IntelRealSense/librealsense
#
#
# git clone https://github.com/IntelRealSense/librealsense
# cd librealsense
# mkdir build
# cd build
# cmake ../ -DBUILD_PYTHON_BINDINGS=TRUE
# make -j4
# sudo make install #Optional if you want the library to be installed in your system

```

### Install ROS

We recommend to install ROS-base first on the board and then install other packages if necessary. If you installed the system on the embedded storage, it would be the best performance to install ROS-Base

```
# Please also check the ROS Website to check the most updated steps to install ROS. (http://wiki.ros.org/kinetic/Installation/Ubuntu)

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update && sudo apt-get install ros-kinetic-ros-base
```
Initialize ROSDEP
```
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
Dependencies for building packages
```
sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential python-catkin-tools python-wstool
sudo pip install -U pip
```
## Development Environment Set up
```
$ mkdir my-workspace && cd my-workspace
$ wstool init src
$ catkin init
$ catkin config --extend /opt/ros/kinetic

```
