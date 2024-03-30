#!/bin/bash

# Date=$(date +'%d-%m-%Y')

ffmpeg -rtsp_transport tcp -i "rtsp://admin:Admin@123@10.15.227.50/Streaming/Channels/$101" -ss 00:00:03 -frames:v 1 -q:v 2 Z479_channel_no_$1.jpg

