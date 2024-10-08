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

from picamera2 import Picamera2
import cv2
import time
from libcamera import ColorSpace
import os

output_file = "output_video.mp4"

if os.path.exists(output_file):
    os.remove(output_file)

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_preview_configuration(main={"size": (1600, 900)})
picam2.configure(config)

pipeline = (
    'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc '
    '! h264parse ! mp4mux ! filesink location=outputvideo.mp4'
)

# output_file = "record_vid.mp4"
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30, (1600, 900))

# Start the camera
picam2.start()

start_time = time.monotonic()
duration = 900

# Allow some time for the camera to adjust to the lighting condition
# time.sleep(2)


while time.monotonic() - start_time < duration:
    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    out.write(frame)
    # Display the live camera feed
    # cv2.imshow("Live Cam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
# cv2.destroyAllWindows()
picam2.stop()

