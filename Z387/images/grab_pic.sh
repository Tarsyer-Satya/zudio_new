#!/bin/bash

# Date=$(date +'%d-%m-%Y')

ffmpeg -rtsp_transport tcp -i "rtsp://admin:Admin@123@10.15.91.50/Streaming/Channels/$101" -ss 00:00:03 -frames:v 1 -q:v 2 Z387_channel_no_$1.jpg

