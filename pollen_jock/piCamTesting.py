from picamera2 import Picamera2
import cv2
import time
from libcamera import ColorSpace

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
# config = picam2.create_preview_configuration(colour_space=ColorSpace.Sycc())
picam2.configure(config)

# Set Auto White Balance (AWB) mode
# picam2.set_controls({
#     "AwbMode": 1
#     })
# picam2.awb_gains = (1.0, 1.4)


# Start the camera
picam2.start()

# Allow some time for the camera to adjust to the lighting condition
time.sleep(2)


while True:
    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Display the live camera feed
    cv2.imshow("Live Cam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()