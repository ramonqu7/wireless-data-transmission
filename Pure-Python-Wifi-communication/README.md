# Python Pure Wifi Communication Test

## These files only used python native wifi library.
### [Socket Python library for Wifi](https://docs.python.org/2/library/socket.html)
<Enter>
 Bandwidth Test Result
 -----
Tested the bandwidth of the connection between laptop and Intel Joule with the python code on the github. The average result is around 100  - 130 Mbps for unverified data transmission.

<Enter>
The code is kivi_test.py, which is a function programmed with kivy GUI python function. It uses the basic socket library to transfer file to another side.
- Protocol is :
  - Server starts listening
  - Client send the file name
  - Server receive the file name and send back
  - Client check whether the name is the same, if so, start sending the file
  - Server receiving the file and save to local
  >One time transmitting buffer size is 10000 bit

- Test result: (Two win10 device) Will do the same test on iot - win10 device later
  - Two device in the same network:
    - File size:1180824 KB (~1GB)
    - Rate: 15.136 Mbps
    - File size:8523 KB (~8MB)
    - Rate: 15.439 Mbps
  - Two device in wifi direct connecting mode
    - File size:1180824 KB (~1GB)
    - Rate: 44.623 Mbps
    - File size:8523 KB (~8MB)
    - Rate: 50.2284 Mbps
  - Two device in wifi direct connecting mode (Laptop to Joule)
    - File size:1180824 KB (~1GB)
    - Rate: 82.678 Mbps/ 49.3536 (haven’t verify the md5)
    - File size:8523 KB (~8MB)
    - Rate: 82.235Mbps
- Astra with Open CV, openni2
  - Tested some example python program and successfully open and fine the 3D nparray data which is going to be transmitted.
  - Send the vision data. Client read it and send the array. The other side receive the array and show the images. (not sure about the time delay and so on)
  ### Openni2 and OpenCV
  [Detail is on this website](https://github.com/PrimeSense/Sensor)
  For Openni2, please check the Python_Openni2 folder Readme.md
  Linux:
	Requirements:
  - 1) GCC 4.x
    - From: http://gcc.gnu.org/releases.htm Or via apt:
    ```
    sudo apt-get install g++
    ```
  - 2)OpenCV
      Please check this [website](https://milq.github.io/install-opencv-ubuntu-debian/)
      ```
      sudo apt-get install libopencv-dev python-opencv
      ```
  - 3) Download Openni2 library
    - In this project, I attached the openni2 driver folder in certain folders.
    - But here is the [link](https://structure.io/openni)
