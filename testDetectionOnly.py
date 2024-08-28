import os
import time
import csv  # Import CSV module to write to CSV files

from ultralytics import YOLO

import cv2
import numpy as np

weights_path = './data/yolov8_models/insects_best_s.pt'

video_path = './data/input/20191123_131057.mp4'
video_path_out = './data/output/20191123_131057_out.mp4'
csv_output_path = './data/output/20191123_131057_detection_counts.csv'  # CSV file path for output

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()
H, W, _ = frame.shape
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc('X','2','6','4'), int(cap.get(cv2.CAP_PROP_FPS)), (W,H))
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


model = YOLO(weights_path)

threshold = 0.5
frame_count = 0  # To keep track of the current frame number
detection_counts = []  # List to store frame number and detection count

while ret:
    frame_count += 1

    results = model(frame)[0]

    detection_count = 0  # Counter for the number of detections in the current frame

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            detection_count += 1
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Append the frame number and detection count to the list
    detection_counts.append([frame_count, detection_count])

    # Write to CSV file every 10 frames
    if frame_count % 10 == 0:
        with open(csv_output_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if frame_count == 10:  # Write the header only once
                writer.writerow(['Frame Number', 'Detection Count'])
            writer.writerows(detection_counts)
        detection_counts = []  # Clear the list after writing to the file

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()

# Write any remaining detection counts to the CSV file after the loop ends
if detection_counts:
    with open(csv_output_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(detection_counts)
