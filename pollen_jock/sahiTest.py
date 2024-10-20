import os
import time
import csv  # Import CSV module to write to CSV files
from ultralytics import YOLO
import cv2
import numpy as np

# SAHI utilities for YOLOv8 instance segmentation
from sahi.utils.yolov8 import (
    download_yolov8s_model, download_yolov8s_seg_model
)
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from IPython.display import Image

# Set paths for YOLOv8 model and video input/output
yolov8_model_path = "../data/yolov8_models/insects_best_s.pt"
video_path = '../data/input/20191123_130028.mp4'
video_path_out = '../data/output/20191123_130028.mp4'
csv_output_path = '../data/output/20191123_130028_detection_counts.csv'  # CSV file path for output

# Download YOLOv8 instance segmentation model
download_yolov8s_seg_model(yolov8_model_path)

# Initialize Video Capture and Writer
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

# Load the YOLOv8 model using SAHI's AutoDetectionModel
detection_model = AutoDetectionModel.from_pretrained(
    model_type="yolov8",
    model_path=yolov8_model_path,
    confidence_threshold=0.6,  # Confidence threshold can be adjusted
    device="cuda"  # Use "cpu" if you don't have GPU support
)

# Initialize frame and detection counters
frame_count = 0
detection_counts = []  # List to store frame number and detection count

while ret:
    frame_count += 1
    
    # Perform slicing inference using SAHI
    result = get_sliced_prediction(
        frame,          # Input frame
        detection_model,          # YOLOv8 model through SAHI
        slice_height=512,   # Slice height, adjust as needed
        slice_width=512,    # Slice width, adjust as needed
        overlap_height_ratio=0.2,  # Overlap between slices (adjust as needed)
        overlap_width_ratio=0.2    # Overlap between slices (adjust as needed)
    )
    
    detection_count = 0  # Counter for the number of detections in the current frame
    
    # Draw bounding boxes and instance segmentation masks
    for obj in result.object_prediction_list:
        x1, y1, x2, y2 = obj.bbox.minx, obj.bbox.miny, obj.bbox.maxx, obj.bbox.maxy
        class_id = obj.category.id
        # Access the score value from the PredictionScore object
        score = obj.score.value if hasattr(obj.score, 'value') else float(obj.score)

        # If confidence score is above the threshold, draw the bounding box
        if score > 0.6:
            detection_count += 1
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            # Draw class label
            cv2.putText(frame, obj.category.name.upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            # Draw segmentation mask (optional)
            if obj.mask is not None:
                mask = obj.mask.bool_mask.astype(np.uint8) * 255
                color = (0, 255, 0)  # Green color for mask
                frame[mask == 255] = color

    # Save the frame with the drawn bounding boxes and masks to the output video
    out.write(frame)
    
    # Store the detection count for this frame
    detection_counts.append([frame_count, detection_count])
    
    # Read the next frame
    ret, frame = cap.read()

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Write detection counts to CSV
with open(csv_output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'Detection Count'])
    writer.writerows(detection_counts)

print(f"Processing completed. Output saved to {video_path_out} and {csv_output_path}.")
