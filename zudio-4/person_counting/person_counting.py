from ultralytics import YOLO
import cv2
# import matplotlib.pyplot as plt
import time
import numpy as np
import argparse
import time
# import cairo
from helper_function_person_counting import *
from datetime import datetime
import os
import json
import numpy as np
# parser = argparse.ArgumentParser(description='A script to process an image')
# parser.add_argument('image', type=str, help='Path to the image file')
# args = parser.parse_args()

store_code = 'Z139'
store_name = 'Tarsyer-Trent-0025'
camera_no = 6


emp_bb = [[0, 372], [0, 720], [837, 720],[923,494],[172,222]]
lane1 = [[172, 222],[923, 494], [1065, 316],[390,83]]
lane2 = [[390, 83], [1065, 316], [1117, 147], [551,0]]

image_path = '/tmp/image.jpg'

# image_path = '/home/satya/Desktop/Tarsyer/Z005-Laxmi road/zudio/Z005-Laxmi road/channel_no_3.jpg'

ALERT_IMAGE_PATH = '/tmp/alert_images/'
os.system(f'mkdir -p {ALERT_IMAGE_PATH}')

json_path = '/tmp/json_data/'
os.system(f'mkdir -p {json_path}')


model = YOLO('yolov8m.pt')  

time_interval = 600

last_executed_time = time.monotonic()-time_interval


while True:


    # run below part after every x seconds

    if abs(time.monotonic()-last_executed_time) > time_interval and get_time_stamp(image_path) > 6:
        last_executed_time = time.monotonic()
            
        start_of_code = time.monotonic()

        img = cv2.imread(image_path)
            
        person_boxes = predict_people(img,model)
        person_boxes_centroid = find_centroids(person_boxes) 

        # plot_image = plot_people(person_boxes,img)
        # plt.imshow(plot_image)
        # plt.show()



        # plt.imshow(roi)

        emp_count,lane1_count, lane2_count = 0,0,0
        for i in range(len(person_boxes)):
            if check(person_boxes_centroid[i], emp_bb):
                emp_count += 1
            if check(person_boxes_centroid[i], lane1):
                lane1_count += 1
            if check(person_boxes_centroid[i], lane2):
                lane2_count += 1

        

        cv2.rectangle(img, (1090,20), (1190,140), (0,255,0) , -1)
        cv2.putText(img, "E-"+str(emp_count), (1100,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        cv2.putText(img, "L1-"+str(lane1_count), (1100,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        cv2.putText(img, "L2-"+str(lane2_count), (1100,130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        

        roi = draw(emp_bb,img)
        roi = draw(lane1,roi)


        
        #plt.imshow(roi)
        #plt.show()

        main_image = cv2.resize(img, (640, 480))

        current_datetime =  datetime.now().strftime("%d-%m-%y_%H-%M-%S")    
        filename_format = f'{current_datetime}_person_count'
        json_name_format = f'{filename_format}.json'
        image_name_format = f'{filename_format}.jpg'

        if lane1_count > 3 or lane2_count > 3 or emp_count == 0:
            cv2.imwrite(f'{ALERT_IMAGE_PATH}{image_name_format}', main_image)

        data = {
            'store_name': store_name,
            'store_code': store_code,
            'camera_no': camera_no,
            'date_time': current_datetime,
            'L1_count': lane1_count,
            'L2_count' : lane2_count,
            'count': emp_count + lane1_count + lane2_count,
            'E_count':emp_count
        }

        # Convert the data to JSON format
        json_data = json.dumps(data, indent=4)

        # Create the full path for the JSON file
        json_file_path = os.path.join(json_path, json_name_format)

        # Write the JSON data to the specified path
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)

        # print(f'Saved to {json_file_path}, count = {emp_count + lane1_count}')

        # print(person_boxes)
        print("Time took in seconds: ", time.monotonic()-start_of_code)

        # cv2.imshow("Image", cv2.resize(roi,(640,480)))
        # Break the loop if 'q' key is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    else:
        time.sleep(600-3)

# bye bye
# cv2.destroyAllWindows()
