import os
import json
import glob
import logging
import time
import requests
import base64

#Creating logging file and configuring it
LOG_FILE_PATH = '/tmp/sending_till_alert.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
logging.info('CODE STARTED')

# Tarsyer server externalIP and Port
url = "http://dashboard.alt1.tarsyer.com:5010/zudio_alert_server"
logging.info(f'URL : {url}')

MOVE_IMAGE = False

###############Image Alerts###############
IMAGE_ALERT_FOLDER_PATH = '/tmp/alert_images/'
if not os.path.exists(IMAGE_ALERT_FOLDER_PATH):
    os.system(f'mkdir -p {IMAGE_ALERT_FOLDER_PATH}')
    logging.info(f'creating folder :{IMAGE_ALERT_FOLDER_PATH}')

IMAGE_ALERT_FOLDER_HOMEDIR = '/home/pi/alert_images/'
if not os.path.exists(IMAGE_ALERT_FOLDER_HOMEDIR):
    os.system(f'mkdir -p {IMAGE_ALERT_FOLDER_HOMEDIR}')
    logging.info(f'creating folder : {IMAGE_ALERT_FOLDER_HOMEDIR}')

image_deleted_folder = '/tmp/deleted_alert_images/'
if not os.path.exists(image_deleted_folder):
    os.system(f'mkdir -p {image_deleted_folder}')
    logging.info(f'creating folder : {image_deleted_folder}')

###############JSON Alerts###############
JSON_ALERT_FOLDER_PATH = '/tmp/json_data/'
if not os.path.exists(JSON_ALERT_FOLDER_PATH):
    os.system(f'mkdir -p {JSON_ALERT_FOLDER_PATH}')
    logging.info(f'creating folder :{JSON_ALERT_FOLDER_PATH}')

JSON_ALERT_FOLDER_HOMEDIR = '/home/pi/json_data/'
if not os.path.exists(JSON_ALERT_FOLDER_HOMEDIR):
    os.system(f'mkdir -p {JSON_ALERT_FOLDER_HOMEDIR}')
    logging.info(f'creating folder : {JSON_ALERT_FOLDER_HOMEDIR}')

json_deleted_folder = '/tmp/deleted_json/'
if not os.path.exists(json_deleted_folder):
    os.system(f'mkdir -p {json_deleted_folder}')
    logging.info(f'creating folder : {json_deleted_folder}')



# defining the header i.e type of payload getting sent and bearer token
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer Tarsyer_CV_2024'
}

"""
alert file name structure :: alert-datetime_location_111.jpg

alert-datetime - 2024-02-01_16-39-00 :: %Y-%m-%d_%H-%M-%S
location - WHRS-Load-Cell

111 - explained below :: 1 - present, 0 - absent
1st - helmet
2nd - suit
3rd - gloves
"""

# This is separate function to check and sent the files present in home dir :: ALERT_FOLDER_HOMEDIR
# It is seperate because logging is different and we don't need to move again and again to the home dir
# ALERT_FOLDER_HOMEDIR_files contains list of all the files present in the home dir

def sending_homedir_files(ALERT_FOLDER_HOMEDIR_files):

    # Iterate through each file in the ALERT_FOLDER_PATH.
    for alert_files in ALERT_FOLDER_HOMEDIR_files:

        # Extract information from the filename for datetime, location, and alert output.
        with open(alert_files, "r") as json_file:
            json_data = json.load(json_file)

        alert_datetime = json_data["date_time"]
        alert_store_name = json_data["store_name"]
        alert_store_code = json_data["store_code"]
        alert_camera_no = json_data["camera_no"]
        alert_count = json_data["count"]
        L1_count = json_data["L1_count"]
        L2_count = json_data["L2_count"]
        E_count = json_data["E_count"]

        if (L1_count > 3) or (L2_count > 3) or (E_count == 0):
            MOVE_IMAGE = True
            # Read the image file in binary mode and convert it to a base64-encoded string.
            alert_image_name = IMAGE_ALERT_FOLDER_HOMEDIR + (alert_files.split('/')[-1]).split('.')[0] + ".jpg"
            with open(alert_image_name, "rb") as img_file:
                alert_img_string = str(base64.b64encode(img_file.read()))
        else:
            MOVE_IMAGE = False
            alert_img_string = "NULL"

        # Create a dictionary containing various details of an alert, such as datetime, location, alert message, and image data.
        alert_string = {
            "date_time": alert_datetime,
            "store_name": alert_store_name,
            "store_code": alert_store_code,
            "camera_no": alert_camera_no,
            "count": alert_count,
            "L1_count": L1_count,
            "L2_count": L2_count,
            "E_count": E_count,
            "alert_image": alert_img_string
        }

        # Convert the dictionary into a JSON-formatted string.
        payload = json.dumps(alert_string)

        # Try to send a POST request to the specified URL with the JSON payload and set a timeout of 10 seconds.
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=60)

            # Log the response text for debugging purposes.
            logging.info(response.text)

            # if "success" in response.text:
            #     # Move the alert files to a 'deleted_folder' after successful transmission.
            #     os.system(f'mv {alert_files} {json_deleted_folder}')
            #
            #     if MOVE_IMAGE:
            #         os.system(f'mv {alert_image_name} {image_deleted_folder}')
            #     logging.info(f'INITIAL: alert file moved to {json_deleted_folder}')
            #
            # else:
            #     logging.info(f'`success` is not present in the response')

        # Handle a timeout exception that might occur during the request.
        except requests.Timeout:
            logging.info(f'INITIAL: ERROR ERROR :: Timeout')

        # Handle other request exceptions and log the error message.
        except requests.RequestException as error:
            logging.info(f'INITIAL: ERROR ERROR :: {error}')

        os.system(f'mv {alert_files} {json_deleted_folder}')

        if MOVE_IMAGE:
            os.system(f'mv {alert_image_name} {image_deleted_folder}')
        logging.info(f'INITIAL: alert file moved to {json_deleted_folder}')


while True:

    # Get a list of all .jpg files in the ALERT_FOLDER_HOMEDIR directory.
    JSON_ALERT_FOLDER_HOMEDIR_files = glob.glob(f'{JSON_ALERT_FOLDER_HOMEDIR}/*.json')
    # Check if the length of the list is not zero.
    if len(JSON_ALERT_FOLDER_HOMEDIR_files) != 0:
        logging.info(f'len of {JSON_ALERT_FOLDER_HOMEDIR_files} is not zero')

        # Call the sending_homedir_files function to handle the files in ALERT_FOLDER_HOMEDIR.
        sending_homedir_files(JSON_ALERT_FOLDER_HOMEDIR_files)

    # Get a list of all .jpg files in the ALERT_FOLDER_PATH directory.
    JSON_ALERT_FOLDER_PATH_files = glob.glob(f'{JSON_ALERT_FOLDER_PATH}/*.json')

    # Iterate through each file in the ALERT_FOLDER_PATH.
    for alert_files in JSON_ALERT_FOLDER_PATH_files:

        # Extract information from the filename for datetime, location, and alert output.
        with open(alert_files, "r") as json_file:
            json_data = json.load(json_file)

        alert_datetime = json_data["date_time"]
        alert_store_name = json_data["store_name"]
        alert_store_code = json_data["store_code"]
        alert_camera_no = json_data["camera_no"]
        alert_count = json_data["count"]
        L1_count = json_data["L1_count"]
        L2_count = json_data["L2_count"]
        E_count = json_data["E_count"]

        if (L1_count > 3) or (L2_count > 3) or (E_count == 0):
            MOVE_IMAGE = True
            # Read the image file in binary mode and convert it to a base64-encoded string.
            alert_image_name = IMAGE_ALERT_FOLDER_PATH + (alert_files.split('/')[-1]).split('.')[0] + ".jpg"
            with open(alert_image_name, "rb") as img_file:
                alert_img_string = str(base64.b64encode(img_file.read()))
        else:
            MOVE_IMAGE = False
            alert_img_string = "NULL"

        # Create a dictionary containing various details of an alert, such as datetime, location, alert message, and image data.
        alert_string = {
            "date_time": alert_datetime,
            "store_name": alert_store_name,
            "store_code": alert_store_code,
            "camera_no": alert_camera_no,
            "count": alert_count,
            "L1_count": L1_count,
            "L2_count": L2_count,
            "E_count": E_count,
            "alert_image": alert_img_string
        }

        # Convert the dictionary into a JSON-formatted string.
        payload = json.dumps(alert_string)


        try:
            # Send a POST request with the payload to the specified URL.
            response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
            logging.info(response.text)
            # if "success" in response.text:
            #     # Move the processed alert file to the deleted_folder.
            #     os.system(f'mv {alert_files} {json_deleted_folder}')
            #     if MOVE_IMAGE:
            #         os.system(f'mv {alert_image_name} {image_deleted_folder}')
            #     logging.info(f'alert file moved to {json_deleted_folder}')
            #
            # else:
            #     logging.info(f'`success` is not present in the response')

        # Handle a timeout exception during the request.
        except requests.Timeout:
            logging.info(f'ERROR ERROR :: Timeout')

            # Move the file to ALERT_FOLDER_HOMEDIR in case of a timeout.
            os.system(f'mv {alert_files} {JSON_ALERT_FOLDER_HOMEDIR}')
            if MOVE_IMAGE:
                os.system(f"mv {alert_image_name} {IMAGE_ALERT_FOLDER_HOMEDIR}")
            logging.info(f'file moved to {JSON_ALERT_FOLDER_HOMEDIR}')

        # Handle other request exceptions and log the error message.
        except requests.RequestException as error:
            logging.info(f'ERROR ERROR :: {error}')

            # Move the file to ALERT_FOLDER_HOMEDIR in case of an exception.
            # os.system(f'mv {alert_files} {JSON_ALERT_FOLDER_HOMEDIR}')
            # if MOVE_IMAGE:
            #     os.system(f"mv {alert_image_name} {IMAGE_ALERT_FOLDER_HOMEDIR}")
            # logging.info(f'file moved to {JSON_ALERT_FOLDER_HOMEDIR}')

        # Move the processed alert file to the deleted_folder.
        os.system(f'mv {alert_files} {json_deleted_folder}')
        if MOVE_IMAGE:
            os.system(f'mv {alert_image_name} {image_deleted_folder}')
        logging.info(f'alert file moved to {json_deleted_folder}')


        # Introduce a delay of 1 second for resting between iterations.
        time.sleep(1)

    # Sleep for 60 seconds after processing all files.
    time.sleep(60)
