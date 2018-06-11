#!/bin/bash
echo "Wait for 3s"
sleep 5s
echo "Start Running"
python3 ./realsense_wrapper/run.py -ip 173.250.184.57 -port 7000
