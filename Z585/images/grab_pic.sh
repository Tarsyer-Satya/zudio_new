#!/bin/bash

# Date=$(date +'%d-%m-%Y')

ffmpeg -rtsp_transport tcp -i "rtsp://admin:Admin123@10.15.192.50/Streaming/Channels/$101" -ss 00:00:03 -frames:v 1 -q:v 2 Z585_channel_no_$1.jpg
