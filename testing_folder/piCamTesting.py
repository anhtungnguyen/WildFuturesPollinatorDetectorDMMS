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

# from picamera2 import Picamera2
import cv2
import time
# from libcamera import ColorSpace
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from GoogleCloud.upload import GoogleServices

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

# Define output dirs
output_dir = "vids"

# Create the output file if it doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate a unique file name based on the current time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_dir, f"output_video_{current_time}.mp4")

# output_file = "output_video.mp4"

# if os.path.exists(output_file):
#     os.remove(output_file)

# Initialize Picamera2
# picam2 = Picamera2()

# Configure the camera
# config = picam2.create_preview_configuration(main={"size": (1600, 900)})
# picam2.configure(config)

# pipeline = (
#     f'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc '
#     f'! h264parse ! mp4mux ! filesink location={output_file}'
# )

# output_file = "record_vid.mp4"
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30, (1600, 900))

# Define recording parameters
frame_rate = 30         # Frame per second
total_seconds = 60    # Total duration in second (1 hour)
total_frame = frame_rate * total_seconds    # Total frames to write

# Start the camera
# picam2.start()

frame_count = 0

# Allow some time for the camera to adjust to the lighting condition
# time.sleep(2)

# Start the cloud session.
gdSession = GoogleServices('pi-test', 'testing_folder\GoogleCloud\service-secrets.json')

while frame_count - total_frame:
    # frame = picam2.capture_array()

    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # out.write(frame)
    # Display the live camera feed
    # cv2.imshow("Live Cam Feed", frame)

    frame_count += 1
    time.sleep(1/frame_rate)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # Send the updated log every 30 seconds (900 frames) with frame count.
    # This is a threaded operation to not interrupt recording.
    if (frame_count % (frame_rate*30)) == 0:
        gdSession.updateLog(f'{frame_count}/{total_frame} frames')
        gdSession.uploadLog()

# out.release()
# cv2.destroyAllWindows()
# picam2.stop()
# send_email_notification()
gdSession.updateLog('Session finished')
gdSession.uploadLog()
gdSession.logThread.join()
