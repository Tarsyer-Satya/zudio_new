#!/bin/bash

# Set the time interval in seconds
time_interval=300

while true; do
    # Your commands go here
    echo "Running your commands at $(date)"
    # ffmpeg -hide_banner -loglevel error -rtsp_transport tcp -ss 00:00:03 -i "rtsp://admin:Admin123@10.0.244.50:554/Streaming/Channels/301" -frames:v 1 -q:v 2 /tmp/image.jpg -y

    ffmpeg -rtsp_transport tcp -i "rtsp://admin:Admin@123@10.15.82.50/Streaming/Channels/901" -ss 00:00:03 -frames:v 1 -q:v 2 /tmp/image.jpg -y
    # Sleep for the specified time interval
    sleep $time_interval
done


