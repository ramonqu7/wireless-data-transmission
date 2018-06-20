## Deploy Joule Demos with ADA

### Steps to Boot the Joule
- Make sure the board is securely mounted in the Joule box. 
- Plug in the power jack.
- Wait for 50 seconds and reset the MicroSD card
> This is an ongoing issue of booting with microSD card. We have to reset the microSD during the booting sequence. Otherwise, the microSD card would not be recognized.
- You are then able to SSH to Joule with 
```
ssh jouleu@192.168.2.176
```
> The other Intel Joule has been set up as `ssh joule@192.168.2.170`

### Start Intel Realsense Camera

- You are able to start the camera by:

```
cd ~
./run_camera.sh
```

> It has been set default that you need to run roscore on weeboo (IP address is `192.168.2.171`)
> If you are running roscore at other machines with different IP address, please specify the IP address before running the script.
> ``` 
> export ROS_MASTER_URI="http://192.168.2.X:11311"
> ```

- You can modify the camera configurations which defined in the Intel RealSense Camera ROS-Wrapper.

```
cd catkin_ws/src/realsense/realsense_camera/launch
```
You may modify the rs_camera.launch file to set the resolution, FPS, enabling camera streams.


### Host machine run point cloud demo

```
source ./devel/setup.bash
roslaunch depth_image_proc cloudify.launch
```

Then you may use `Rviz` to view the point cloud data with subscribing to **Topic** `/camera/color/depth/points`

## Ongoing issues:

- Color/Depth Synchronization Problem

    The `color` and `aligned depth to color` frames may not arrive at the same time. `point_cloud_xyz_rgb` use `message_filter` and checking the `frame_id` to sync two frames. However, it would continuously give the error that two frame ids are not the same, which would not reconstruct the point cloud data.


   > _We have disabled the commands which checking the frame id._
   > _But we are also working on other solutions to make the frame synchronization issue._


- Using Image Transport

    The local reconstruct point cloud requires `Color` and `aligned_depth_to_color` frames. We applied `Compressed Image Transport` on the color frames and `CompressedDepth Image transport` on the depth (Aligned depth to color) frames. 

    But in order to make the wireless transmission smoothly, we may need to set the dynamic parameters of the transport, like the compression quality. 

    ```
    #After running the camera on the joule site, open another ssh window to joule.
    rosrun dynamic_reconfigure dynparam set /camera/color/image_raw/compressed jpeg_quality 70
    rosrun dynamic_reconfigure dynparam set /camera/aligned_depth_to_color/image_raw/compressedDepth png_level 7
    ```
