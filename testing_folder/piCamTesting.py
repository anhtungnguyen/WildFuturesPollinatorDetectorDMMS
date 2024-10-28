# from picamera2 import Picamera2
# import cv2
# import time
# from libcamera import ColorSpace

# # Initialize Picamera2
# picam2 = Picamera2()

# # Configure the camera
# config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
# picam2.configure(config)

# frame_width = 1920
# frame_height = 1080
# frame_rate = 30

# output_file = "record_vid.mp4"
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# out = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

# # Start the camera
# picam2.start()

# start_time = time.time()
# duration = 60

# # Allow some time for the camera to adjust to the lighting condition
# # time.sleep(2)


# while time.time() - start_time < duration:
#     frame = picam2.capture_array()

#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#     out.write(frame)
#     # Display the live camera feed
#     # cv2.imshow("Live Cam Feed", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# out.release()
# cv2.destroyAllWindows()
# picam2.stop()

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

import threading
import numpy as np

# from systemd import daemon

# Hailo imports
from picamera2.devices import Hailo

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

def send_image(frame_in, time, name="raw"):
    # Send an image to the google drive folder. Note that these are not currently sorted into folders on the Google Drive.
    # Images to be sent are raws, bee detections, all detections. -> when a pollination event is detected.

    # Save locally
    image_name = f'{output_dir_imgs}/{time}_{name}.png'
    cv2.imwrite(f'{image_name}', frame_in)

    # Upload.
    gdSession.upload(image_name)

def get_bb_frame(frame_in, detections):
    if detections:
        bb_frame = np.copy(frame_in)
        for class_name, bbox, score in detections:
            x0, y0, x1, y1 = bbox
            label = f"{class_name} {int(score*100)}%"
            bb_frame = cv2.rectangle(bb_frame, (int((x0)), int((y0))), (int((x1)), int((y1))), (0, 255, 0, 125), 2)
            bb_frame = cv2.putText(bb_frame, label, (int((x0)+5), int((y0)+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 125), 1, cv2.LINE_AA)
        return bb_frame
    return frame_in
    
def extract_detections(hailo_output, w, h, class_names, threshold=0.5):
    results = []
    for class_id, detections in enumerate(hailo_output):
        for detection in detections:
            score = detection[4]
            if score >= threshold:
                y0, x0, y1, x1 = detection[:4]
                bbox = (int(x0*w), int(y0*h), int(x1*w), int(y1*h))
                results.append([class_names[class_id], bbox, score])
    return results

# Define output dirs
output_dir = f'{os.getcwd()}/vids/field'

# Create the output file if it doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate a unique file name based on the current time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_dir, f"output_video_{current_time}.mp4")
print("Saving to ", output_file)
# output_file = "output_video.mp4"

# if os.path.exists(output_file):
#     os.remove(output_file)


# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_video_configuration(main={"size": (1600, 900)})
picam2.configure(config)

pipeline = (
    f'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc '
    f'! h264parse ! mp4mux ! filesink location={output_file}'
)

# Initialise the Google Drive.
# print(os.getcwd())
gdSession = GoogleServices('field', f'{os.getcwd()}/GoogleCloud/service-secrets.json')

# output_file = "record_vid.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

#out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30, (1600, 900)) 
# out = cv2.VideoWriter(output_file, fourcc, 30, (1600, 900), True) 

# if not out.isOpened():
#     print('video writer not opened')

# Connect to Hailo AI Kit
hailo = Hailo(f"{os.getcwd()}/models/hybrid.hef")
# print(hailo.get_input_shape())
model_h, model_w, _ = hailo.get_input_shape() # e.g. (640, 640, 3)
video_w, video_h = 1600, 900

# Read class list (bee, flower)
with open(f"{os.getcwd()}/models/hybrid.txt", 'r', encoding="utf-8") as f:
    class_names = f.read().splitlines()

# Set detections to None to start.
detections = None

# Define recording parameters
frame_rate = 30         # Frame per second
total_seconds = 1800    # Total duration in seconds (1/2 hour)
total_frame = frame_rate * total_seconds    # Total frames to write

# Start the camera
# picam2.start()

frame_count = 0

# Create a directory to store images taken during detections. Images to be stored (raw, bee only, all detections). To be taken during pollination events.
output_dir_imgs = f'{os.getcwd()}/imgs/{current_time}'
if not os.path.exists(output_dir_imgs):
    os.makedirs(output_dir_imgs)

# Allow some time for the camera to adjust to the lighting condition
time.sleep(2)

video_path = f'{os.getcwd()}/beeVids/batch2/20241019_112830.mp4'
cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()
video_h, video_w, _ = frame.shape
out = cv2.VideoWriter(output_file, fourcc, 30, (video_w, video_h), True) 

# send_start_email_notification()
try:
    while ret: 
    # while frame_count - total_frame: # Recording should be changed to indefinite. Only save to file for specified number of frames when possible bee detected.
        # daemon.notify("WATCHDOG=1")
        detections = None
        # frame = picam2.capture_array() # get frame as numpy array.

        frame_input = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # vidThread = threading.Thread(target=out.write, args=([frame]))
        # vidThread.start()
        # out.write(frame)
 
        # Display the live camera feed
        # cv2.imshow("Live Cam Feed", frame)

        frame_count += 1

        # Email notification handling.
        # if (frame_count == int(total_frame)/100):
        #     send_early_email_notification()

        # if (frame_count == int(total_frame)/10):
        #     send_early_email_notification()

        # if (frame_count == int(total_frame)/3*2):
        #     send_early_email_notification()

        # if (frame_count == int(total_frame / 4)):
        #     send_half_email_notification()
        

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # AI logic goes here.
        # Downsize the frame for AI input.
        frame_input = cv2.resize(frame_input, (model_w,model_h))
        results = hailo.run(frame_input)
        detections = extract_detections(results[0], video_w, video_h, class_names, 0.4) 
        # print(detections)

        # Based on detections, if pollination event detected, send  bb_frame to google drive.
        bb_frame = get_bb_frame(frame, detections)

        vidThread = threading.Thread(target=out.write, args=([bb_frame]))
        vidThread.start()


        # If detections are made, upload files here. Uploading should be threaded so loop does not wait for it to finish.
        if (frame_count % (frame_rate*5)) == 0: # Send an updated log every minute.
            gdSession.updateLog(f"{frame_count} frames processed")
            gdSession.uploadLog() # Threaded upload of log file.

            # Upload the current frame. In the future this should be a frame of pollination detections.
            det_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
            raw_thread = threading.Thread(target=send_image, args=(frame, det_time, "raw"))
            raw_thread.start()
            if detections:
                det_thread = threading.Thread(target=send_image, args=(bb_frame, det_time, "det"))
                det_thread.start()

        vidThread.join()
        ret, frame = cap.read()
    gdSession.updateLog("Recording Stopped")
    gdSession.uploadLog() # Threaded upload of log file.
    gdSession.logThread.join()

except Exception as error:
    print("Failure: ", error)
    gdSession.updateLog(f"{frame_count}/{total_frame} frames processed at error")
    gdSession.updateLog(f"Failure: {error}")
    gdSession.uploadLog() # Threaded upload of log file.
    gdSession.logThread.join()
print("Recording halted.")

cap.release()
out.release()
# cv2.destroyAllWindows()
# picam2.stop()
# send_email_notification()

