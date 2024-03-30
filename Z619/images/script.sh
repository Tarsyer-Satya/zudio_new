#!/bin/bash



ffmpeg -rtsp_transport tcp -ss 00:00:03 -i "rtsp://admin:Admin123@10.15.161.50:554/Streaming/Channels/$101" -frames:v 1 -q:v 2 channel_no_$1.jpg