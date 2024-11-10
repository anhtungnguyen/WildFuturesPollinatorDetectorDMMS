from picamera2 import Picamera2, MappedArray, Preview
import cv2
import time
from libcamera import ColorSpace
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Drive Imports
from GoogleCloud.upload import GoogleServices

# Tracker imports
from Tracking.pollination import update_tracked_bees, is_bee_on_flower

import threading
import numpy as np

# from systemd import daemon

# Hailo imports
from picamera2.devices import Hailo

# For deleting data folders
import shutil

# For using csvs.
import csv

def send_email_notification():
    # Email configuration
    sender_email = "tungnguyen68mufc@gmail.com"
    receiver_email = "anhtungnguyen1809@gmail.com"
    password = "ichk ydiq alcv govd"

    subject = "Raspberry Pi Notification - Video Recording Completed"
    body = "DONE RECORDING"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_start_email_notification():
    # Email configuration
    sender_email = "tungnguyen68mufc@gmail.com"
    receiver_email = "anhtungnguyen1809@gmail.com"
    password = "ichk ydiq alcv govd"

    subject = "Raspberry Pi Notification - Video Recording Started"
    body = "START RECORDING"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for attempt in range(3):
        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print("Email notification sent successfully.")
            break
        except Exception as e:
            print(f"Failed to send email notification: {e}")
            if attempt < 2:  # Wait before retrying, if not the last attempt
                time.sleep(2)

def send_half_email_notification():
    # Email configuration
    sender_email = "tungnguyen68mufc@gmail.com"
    receiver_email = "anhtungnguyen1809@gmail.com"
    password = "ichk ydiq alcv govd"

    subject = "Raspberry Pi Notification - Video Recording Completed"
    body = "QUAD DONE"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_early_email_notification():
    # Email configuration
    sender_email = "tungnguyen68mufc@gmail.com"
    receiver_email = "anhtungnguyen1809@gmail.com"
    password = "ichk ydiq alcv govd"

    subject = "Raspberry Pi Notification - Video Recording Just Started"
    body = "RECORDING"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_email_notification(receiver, subject_line, body_text):
    # Email configuration
    sender_email = "pollenjocks.wildfutures@gmail.com"
    receiver_email = " ,".join(receiver) # If sending to multiple recipients, make a list of email addresses -> ['email@gmail.com', 'email2@gmail.com']
    password = "pojm jnek bosc qgmq"

    subject = subject_line
    body = body_text

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        # text = msg.as_string()
        # server.sendmail(sender_email, receiver_email, text)
        server.send_message(msg)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_image(frame_in, time, name="raw"):
    # Send an image to the google drive folder. Note that these are not currently sorted into folders on the Google Drive.
    # Images to be sent are raws, bee detections, all detections. -> when a pollination event is detected.

    # Save locally
    image_name = f'{output_dir_imgs}/{time}_{name}.png'
    cv2.imwrite(f'{image_name}', frame_in)

    # Upload.
    gdSession.upload(image_name)

def get_bb_frame(frame_in, bees, flowers, pollination_list):
    if bees or flowers:
        bb_frame = np.copy(frame_in)
        for index, (class_name, bbox, score) in enumerate(bees):
            x0, y0, x1, y1 = bbox
            # If detection is a bee and pollination list is 1, make frame red and change label.
            if ((class_name == class_names[0]) and (pollination_list[index] == 1)):
                label = f"{class_name} poll. {int(score*100)}%"
                bb_frame = cv2.rectangle(bb_frame, (int((x0)), int((y0))), (int((x1)), int((y1))), (0, 0, 255, 125), 2)
                bb_frame = cv2.putText(bb_frame, label, (int((x0)+5), int((y0)+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 125), 1, cv2.LINE_AA)
            else: # Otherwise mark as green.
                label = f"{class_name} {int(score*100)}%"
                bb_frame = cv2.rectangle(bb_frame, (int((x0)), int((y0))), (int((x1)), int((y1))), (0, 255, 0, 125), 2)
                bb_frame = cv2.putText(bb_frame, label, (int((x0)+5), int((y0)+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 125), 1, cv2.LINE_AA)
        for class_name, bbox, score in flowers:
            x0, y0, x1, y1 = bbox
            label = f"{class_name} {int(score*100)}%"
            bb_frame = cv2.rectangle(bb_frame, (int((x0)), int((y0))), (int((x1)), int((y1))), (0, 255, 0, 125), 2)
            bb_frame = cv2.putText(bb_frame, label, (int((x0)+5), int((y0)+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 125), 1, cv2.LINE_AA)            
        return bb_frame
    return frame_in
    
def extract_detections(hailo_output, w, h, class_names, threshold=0.5):
    results_bee = []
    results_flower = []
    for class_id, detections in enumerate(hailo_output):
        for detection in detections:
            score = detection[4]
            if score >= threshold:
                # The bounding box parameters.
                y0, x0, y1, x1 = detection[:4]
                bbox = (int(x0*w), int(y0*h), int(x1*w), int(y1*h))
                # Decide which array to put the detection into.
                if class_id: # Flower detected (1)
                    results_flower.append([class_names[class_id], bbox, score])
                else: # Bee detected (0)
                    results_bee.append([class_names[class_id], bbox, score])
    return results_bee, results_flower

def upload_video(path, name):

    # Upload video. This function is to be used threaded.
    vid_data = gdSession.drive.CreateFile({'title' : f'{name}.mp4', 'parents' : [{'id' : gdSession.sessionFolder}]}) # Create local file reference.
    vid_data.SetContentFile(path) # Set content reference to be newly created csv file.

    vid_data.Upload() # Upload to cloud

    # Delete file. 
    os.remove(path)

# Define output dirs
# output_dir = f'{os.getcwd()}/vids'

# Create the output file if it doesnt exist
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

time.sleep(5) # Wait for time to be correct.

# Generate a unique file name based on the current time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# output_file = os.path.join(output_dir, f"output_video_{current_time}.mp4")
# print("Saving to ", output_file)

# if os.path.exiscsvts(output_file):
#     os.remove(output_file)


# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_video_configuration(main={"size": (1920, 1080)})
picam2.configure(config)

# pipeline = (
#     f'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc '
#     f'! h264parse ! mp4mux ! filesink location={output_file}'
# )

# Initialise the Google Drive.
# print(os.getcwd())
gdSession = None
while gdSession == None:
    time.sleep(0.1)
    print(' . ')
    try:
        gdSession = GoogleServices('pi', f'{os.getcwd()}/GoogleCloud/service-secrets.json')
    except Exception as error:
        print('Cloud Failure: ', error)
        continue

try:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out_raw = None
    out_det = None

    # out = cv2.VideoWriter(output_file, fourcc, 30, (1920, 1080), True) # Recording template.

    # if not out.isOpened():
        # print('video writer not opened')

    # Connect to Hailo AI Kit
    hailo = Hailo(f"{os.getcwd()}/models/hybrid.hef")
    # print(hailo.get_input_shape())
    model_h, model_w, _ = hailo.get_input_shape() # e.g. (640, 640, 3)
    video_w, video_h = 1920, 1080

    # Read class list (bee, flower)
    with open(f"{os.getcwd()}/models/hybrid.txt", 'r', encoding="utf-8") as f:
        class_names = f.read().splitlines()

    # Define recording parameters
    frame_rate = 30         # Frame per second
    # total_seconds = 1800    # Total duration in seconds (1/2 hour)
    # total_frame = frame_rate * total_seconds    # Total frames to write

    # Start the camera
    picam2.start()

    frame_count = 0

    # Delete all images from the last session. 
    image_folder = f'{os.getcwd()}/imgs'
    if os.path.exists(image_folder):
        shutil.rmtree(image_folder)

    # Create a directory to store images taken during detections. Images to be stored (raw, bee only, all detections). To be taken during pollination events.
    output_dir_imgs = f'{os.getcwd()}/imgs/{current_time}'
    if not os.path.exists(output_dir_imgs):
        os.makedirs(output_dir_imgs)

    # Alternatively, take videos for capture. 
    # Delete all videos from the last session. 
    vid_folder = f'{os.getcwd()}/vids'
    if os.path.exists(vid_folder):
        shutil.rmtree(vid_folder)

    # Create directory to store videos taken during detections. 
    output_dir_vids = f'{os.getcwd()}/vids/{current_time}'
    if not os.path.exists(output_dir_vids):
        os.makedirs(output_dir_vids)

    # Create a folder to hold csvs for this session. Also erase old csvs.
    csv_folder = f'{os.getcwd()}/csvs'
    if os.path.exists(csv_folder):
        shutil.rmtree(csv_folder)

    csv_folder = f'{os.getcwd()}/csvs/{current_time}'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Initialise the csv file directory for this session.
    csv_file = csv_folder + f'/{current_time}.csv'

    # Make csv file headings.
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'Frame', 'Bee Count', 'Pollination Count', 'Flower Count'])
        csvfile.close()

    # Upload csv and get its cloud storage id to be continuously updated.
    csv_data = gdSession.drive.CreateFile({'title' : f'{current_time}_csv.csv', 'parents' : [{'id' : gdSession.sessionFolder}]}) # Create local file reference.
    csv_data.SetContentFile(csv_file) # Set content reference to be newly created csv file.

    csv_data.Upload() # Upload to cloud
    csv_id = None
    while csv_id == None: # Wait for CSV to be uploaded.
        time.sleep(0.1)
        csv_id = gdSession.getIdOfTitle(f'{current_time}_csv.csv', gdSession.sessionFolder)
        print(' . ')
    print('CSV File ID: ' + str(csv_id)) # Print the found id
    csv_data = gdSession.drive.CreateFile({'title' : f'{current_time}_csv.csv', 'parents' : [{'id' : gdSession.sessionFolder}], 'id' : csv_id}) # Create new local reference with cloud id.

    # Allow some time for the camera to adjust to the lighting condition
    time.sleep(2)

    #
    vid_raw = None
    vid_det = None

    # Attempt to download the config.yaml from the Shared Drive.
    config_id = None
    download_attempts = 0
    while config_id == None:
        time.sleep(0.1)
        config_id = gdSession.getIdOfTitle('config.yaml', gdSession.topFolder)
        print('.')
        download_attempts += 1
        if download_attempts > 10:
            break
    if config_id: # If we successfully got the content id, get its contents and load into session config.
        config = gdSession.downloadConfig(config_id)
        # print(config)
        max_distance = config['max_distance']
        checkpoint_minutes = config['checkpoint_minutes']
        poll_seconds = config['pollination_seconds']
        det_threshold = config['detection_threshold']

        vid_notif_level = config['video_notification_level']
        vid_notif_frequency_sec = config['video_notification_frequency_seconds']
        vid_notif_length = config['video_notification_length_seconds']
        
        email_notif_level = config['email_notification_level']
        email_notif_frequency_min = config['email_notification_frequency_minutes']
        mail_list = ["pollenjocks.wildfutures@gmail.com"]
        mail_list.extend(config['mail_list'])
    else: # Otherwise, use default configs.
        max_distance = 75
        checkpoint_minutes = 15
        poll_seconds = 1
        det_threshold = 0.5

        vid_notif_level = 1
        vid_notif_frequency_sec = 60
        vid_notif_length = 10
        
        email_notif_level=1
        email_notif_frequency_min = 60
        mail_list = ["pollenjocks.wildfutures@gmail.com"]


    tracked_bees = []
    tracked_flowers = []
    # max_distance = 75 # Max distance for matching bees using spatial tracker.
    # checkpoint_minutes=15 # How many minutes before uploading check-in images and log upload.
    # poll_seconds = 1 # For how many seconds should a bee bee on a flower for a polination event.
    # det_threshold = 0.5

    # Image configs for alerts to Google Drive. 
    # vid_notif_level=1 # Alert level trigger for images. 0 - no images. 1 - only for pollination events. 2 - for any bee detections.
    # vid_notif_frequency_sec=60
    vid_notif_cooldown=False # is the image notification function on cooldown?
    vid_notif_frame=0 # the last frame that the image notif function was triggered.

    # Video configs
    # vid_notif_length = 10 # Default to 10.
    vid_notif_stop_rec = False

    # Email configs for alerts.
    # email_notif_level = 1 # Alert level trigger for emails. 0 - no emails. 1 - only for pollination events. 2 - for any bee detections. 
    # email_notif_frequency_min=60
    email_notif_cooldown=False # is the email function on cooldown?
    email_notif_frame=0 # the last frame that the email function was triggered.
    # mail_list = ["pollenjocks.wildfutures@gmail.com"] # Should always at least email to self.

# try:
    # while ret: 
    while True:#frame_count - total_frame: # Recording should be changed to indefinite. Only save to file for specified number of frames when possible bee detected.
        # daemon.notify("WATCHDOG=1")
        bee_det = None
        flower_det = None
        tracked_flowers = []
        frame = picam2.capture_array() # get frame as numpy array.

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # vidThread = threading.Thread(target=out.write, args=([frame]))
        # vidThread.start()
        # out.write(frame)
 
        # Display the live camera feed
        # cv2.imshow("Live Cam Feed", frame)

        frame_count += 1

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # AI logic goes here.
        # Downsize the frame for AI input.
        frame_input = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), (model_w,model_h))
        results = hailo.run(frame_input)

        # Sort detections into arrays of bees and flowers. Also define confidence threshold.
        bee_det, flower_det = extract_detections(results[0], video_w, video_h, class_names, det_threshold) 

        new_tracked_bees = []

        detection_count = 0

        for result in bee_det:
            name, (x0, y0, x1, y1), score = result
            # results_bee.append([class_names[class_id], bbox, score])
            mid_x = int((x0+x1)/2)
            mid_y = int((y0+y1)/2)
            area = int(abs((x0-x1) * (y0-y1)))
            new_tracked_bees.append([mid_x, mid_y, area, 0, score, 0])
            # middle x, middle y, area of box, class id, confidence score, frame count on flower

        # Match new bee detections to old bee detections.
        tracked_bees = update_tracked_bees(tracked_bees, new_tracked_bees, max_distance)

        for result in flower_det:
            name, (x0, y0, x1, y1), score = result
            mid_x = int((x0+x1)/2)
            mid_y = int((y0+y1)/2)
   
            # Calculate radius of minimum enclosing circle
            dx = x1 - mid_x
            dy = y1 - mid_y
            radius = np.sqrt(dx**2 + dy**2) / 2
            # Should tracked_flowers be emptied for every frame? We aren't really tracking them.
            tracked_flowers.append([mid_x, mid_y, radius, 1, score])

        # Now, determine which bees are pollinating flowers and increment
        # the flower counter. Returns which bees are pollinating.
        # valid_bees has been changed to an array of 0s and 1s whose index corresponds
        # to the index of each bee in bee_det. 0 represent no pollination and 1
        # represents pollination. We use this to colour boxes accordingly. 
        valid_bees = is_bee_on_flower(tracked_bees, tracked_flowers, frame_rate*poll_seconds)

        # Based on detections, if pollination event detected, send bb_frame to google drive.
        # if bee_det:
        # print(bee_det)
        # print(tracked_bees)
        # print(valid_bees)
        bb_frame = get_bb_frame(frame, bee_det, flower_det, valid_bees)

        # vidThread = threading.Thread(target=out.write, args=([bb_frame]))
        # vidThread.start()

        # Write to videos.
        if (vid_notif_cooldown == True) and ((frame_count - vid_notif_frame) % (frame_rate*vid_notif_length) != 0):
            vidThread_raw.join()
            vidThread_det.join()

            vidThread_raw = threading.Thread(target=out_raw.write, args=([frame]))
            vidThread_raw.start()
            vidThread_det = threading.Thread(target=out_det.write, args=([bb_frame]))
            vidThread_det.start()
        elif (vid_notif_stop_rec == False) and (vid_notif_cooldown == True) and ((frame_count - vid_notif_frame) % (frame_rate*vid_notif_length) == 0): # Upload videos.
            # When set time is over, .release() each video, upload, (and set vid_raw, vid_det out_raw, out_det to None?)
            vid_notif_stop_rec = True
            
            vidThread_raw.join()
            vidThread_det.join()

            out_raw.release()
            out_det.release()

            upload_raw = threading.Thread(target=upload_video, args=([vid_raw, f'{det_time}_raw']))
            upload_det = threading.Thread(target=upload_video, args=([vid_det, f'{det_time}_det']))

            upload_raw.start()
            upload_det.start()

        # Check if any currently on notification cooldowns should be switched off.
        if (vid_notif_cooldown == True) and ((frame_count - vid_notif_frame) % (frame_rate*vid_notif_frequency_sec) == 0):
            vid_notif_cooldown = False # Cooldown off on images.
        if (email_notif_cooldown == True) and ((frame_count - email_notif_frame) % (frame_rate*60*email_notif_frequency_min) == 0):
            email_notif_cooldown = False # Cooldown off on emails

        # Every n minutes, upload a raw image and detection image to show current state of camera.
        # Also, log progress in the log file.
        if (frame_count % (frame_rate*60*checkpoint_minutes)) == 0: # Default is 15 minutes.
            checkpoint_time = datetime.now().strftime("%d_%H:%M:%S")
            gdSession.updateLog(f"{frame_count} frames processed at target interval of {checkpoint_minutes} minutes.")
            gdSession.uploadLog()

            # Upload the raw frame and detection frame. Note that the detection frame may have no detections on it, which is stil useful information.
            raw_checkpoint = threading.Thread(target=send_image, args=(frame, checkpoint_time, "condition_raw"))
            det_checkpoint = threading.Thread(target=send_image, args=(bb_frame, checkpoint_time, "condition_det"))
            raw_checkpoint.start()
            det_checkpoint.start()

            # Upload the CSV data.
            csv_data.SetContentFile(csv_file) # Set content reference to be newly created csv file.
            csv_thread = threading.Thread(target=csv_data.Upload())
            csv_thread.start()

        # Count the number of bees, flowers, and pollination events detected.
        no_poll_events = valid_bees.count(1) # Occurence of 1 indicate an individual pollination event.
        no_bees = len(valid_bees) # There will be as many bee detections as the length of the valid bees list.
        no_flowers = len(flower_det)

        # Write to csv each second (not frame? too much data?) the timestamp, frame count, number of bees, number of pollination events, number of flowers
        if (frame_count % frame_rate) == 0:
            with open(csv_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), frame_count, no_bees, no_poll_events, no_flowers])
                csvfile.close()
        

        # If there are any bee detections at an interval of n seconds (think like a cooldown). Default is 10 seconds.
        # If there are any 1 - pollinations, 2 - bees, 3 - pollinations or bees, upload a raw and detection image.
        if (not vid_notif_cooldown) and (vid_notif_level != 0):
            if (vid_notif_level == 1) and no_poll_events: # Send only images of pollinations.
                # Get the upload thread for the raw image going.
                det_time = datetime.now().strftime("%d_%H:%M:%S")
                # raw_thread = threading.Thread(target=send_image, args=(frame, det_time, "raw"))
                # raw_thread.start()

                # Upload the detection frame.
                # det_thread = threading.Thread(target=send_image, args=(bb_frame, det_time, "det"))
                # det_thread.start()
                vid_notif_cooldown = True # Set cooldown
                vid_notif_frame = frame_count # Set cooldown start to current frame
                # gdSession.updateLog(f"Images sent for pollination event.")
                gdSession.updateLog(f"Video now recording for pollination event.")

                vid_raw = f'{output_dir_vids}/{det_time}_raw.mp4'
                vid_det = f'{output_dir_vids}/{det_time}_det.mp4'

                out_raw = cv2.VideoWriter(vid_raw, fourcc, 30, (1920, 1080), True)
                out_det = cv2.VideoWriter(vid_det, fourcc, 30, (1920, 1080), True)

                # Write the first frames. Continue this when checking truth of cooldown.
                # When set time is over, .release() each video, upload, and set vid_raw, vid_det out_raw, out_det to None.
                vidThread_raw = threading.Thread(target=out_raw.write, args=([frame]))
                vidThread_raw.start()
                vidThread_det = threading.Thread(target=out_det.write, args=([bb_frame]))
                vidThread_det.start()
                vid_notif_stop_rec = False


            elif (vid_notif_level == 2) and no_bees: # Send only images of bees.
                # Get the upload thread for the raw image going.
                det_time = datetime.now().strftime("%d_%H:%M:%S")
                # raw_thread = threading.Thread(target=send_image, args=(frame, det_time, "raw"))
                # raw_thread.start()

                # Upload the detection frame.frame_rate
                # det_thread = threading.Thread(target=send_image, args=(bb_frame, det_time, "det"))
                # det_thread.start()
                vid_notif_cooldown = True # Set cooldown
                vid_notif_frame = frame_count # Set cooldown start to current frame
                gdSession.updateLog(f"Video now recording for bee detection.")

                vid_raw = f'{output_dir_vids}/{det_time}_raw.mp4'
                vid_det = f'{output_dir_vids}/{det_time}_det.mp4'

                out_raw = cv2.VideoWriter(vid_raw, fourcc, 30, (1920, 1080), True)
                out_det = cv2.VideoWriter(vid_det, fourcc, 30, (1920, 1080), True)

                # Write the first frames. Continue this when checking truth of cooldown.
                # When set time is over, .release() each video, upload, and set vid_raw, vid_det out_raw, out_det to None.
                vidThread_raw = threading.Thread(target=out_raw.write, args=([frame]))
                vidThread_raw.start()
                vidThread_det = threading.Thread(target=out_det.write, args=([bb_frame]))
                vidThread_det.start()
                vid_notif_stop_rec = False


            # elif (img_notif_level == 3) and (no_bees or no_poll_events): # This is for condition 3, but applies for undefined behaviour as well.
            #     # Get the upload thread for the raw image going.
            #     det_time = datetime.now().strftime("%d_%H:%M:%S")
            #     raw_thread = threading.Thread(target=send_image, args=(frame, det_time, "raw"))
            #     raw_thread.start()

            #     # Upload the detection frame.
            #     det_thread = threading.Thread(target=send_image, args=(bb_frame, det_time, "det"))
            #     det_thread.start()
            #     img_notif_cooldown = True # Set cooldown
            #     img_notif_frame = frame_count # Set cooldown start to current frame
            #     gdSession.updateLog(f"Images sent for bee or pollination event.")
            

        # Email notification function. If there are any 1 - pollinations, 2 - bees, 3 - pollinations or bees, send an email.
        # This also uses a cooldown in minutes to avoid spam.
        if (not email_notif_cooldown) and (email_notif_level != 0):
            if (email_notif_level == 1) and no_poll_events: # Pollinations only
                sub = "Pollen Jocks - Pollination Event Detected"
                body = f"""Hello, \n \n A pollination event has been detected, triggering this email. \n 
                \n 
                Current number of pollination events: {no_poll_events} \n 
                Current number of bees detected: {no_bees} \n 
                Current number of flowers detected: {no_flowers} \n 
                \n 
                Regards, \n 
                Pollen Jocks
                """
                email_thread = threading.Thread(target=send_email_notification, args=(mail_list, sub, body))        
                email_thread.start()
                email_notif_cooldown = True
                email_notif_frame = frame_count
                gdSession.updateLog(f"Emails sent for pollination event.")

            elif (email_notif_level == 2) and no_bees: # Bees only
                sub = "Pollen Jocks - Bee Detected"
                body = f"""Hello, \n \n A bee has been detected, triggering this email. \n 
                \n 
                Current number of pollination events: {no_poll_events} \n 
                Current number of bees detected: {no_bees} \n 
                Current number of flowers detected: {no_flowers} \n 
                \n 
                Regards, \n 
                Pollen Jocks
                """
                email_thread = threading.Thread(target=send_email_notification, args=(mail_list, sub, body))        
                email_thread.start()
                email_notif_cooldown = True
                email_notif_frame = frame_count
                gdSession.updateLog(f"Emails sent for bee detection.")

            # elif (email_notif_level == 3) and (no_bees or no_poll_events): # This is for condition 3.
            #     sub = "Pollen Jocks - Pollination/Bee Event Detected"
            #     body = f"""Hello, \n \n A pollination or bee event has been detected, triggering this email. \n 
            #     \n 
            #     Current number of pollination events: {no_poll_events} \n 
            #     Current number of bees detected: {no_bees} \n 
            #     Current number of flowers detected: {no_flowers} \n 
            #     \n 
            #     Regards, \n 
            #     Pollen Jocks
            #     """
            #     email_thread = threading.Thread(target=send_email_notification, args=(mail_list, sub, body))        
            #     email_thread.start()
            #     email_notif_cooldown = True
            #     email_notif_frame = frame_count
            #     gdSession.updateLog(f"Emails sent for pollination even t or bee detection.")


        # vidThread.join()
        # ret, frame = cap.read()

except Exception as error:
    print("Failure: ", error)
    gdSession.updateLog(f"{frame_count} frames processed at error")
    gdSession.updateLog(f"Failure: {error}")
    gdSession.uploadLog() # Threaded upload of log file.
    gdSession.logThread.join()
print("Recording halted.")
gdSession.updateLog("Recording Stopped")
gdSession.uploadLog() # Threaded upload of log file.
gdSession.logThread.join()

# cap.release()
# out.release()
# cv2.destroyAllWindows()
picam2.stop()
# send_email_notification()

