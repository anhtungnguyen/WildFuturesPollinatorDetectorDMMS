
import os
import time
import csv  # Import CSV module to write to CSV files

import cv2
import numpy as np
import copy
from copy import deepcopy
import math
import yaml

# Load the config file
def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Function to update tracked bees instead of resetting
def update_tracked_bees(bees, new_bees, max_distance=50):
    updated_bees = []
    for new_bee in new_bees:
        bee_x, bee_y, new_area, new_class_id, new_score, _ = new_bee
        matched = False
        for bee in bees:
            old_bee_x, old_bee_y, old_area, old_class_id, old_score, frame_count = bee
            distance = math.sqrt((bee_x - old_bee_x)**2 + (bee_y - old_bee_y)**2)
            if distance < max_distance:  # Match based on proximity
                matched = True
                # Update the position and increment the frame count
                updated_bees.append([bee_x, bee_y, new_area, new_class_id, new_score, frame_count])
                break
        
        if not matched:
            # If no match, it's a new bee
            updated_bees.append([bee_x, bee_y, new_area, new_class_id, new_score, 0])

    return updated_bees

# Function to check if a bee is on a flower for at least 1 second
def is_bee_on_flower(bees, flowers, frame_threshold=30):
    valid_bees = []
    for bee in bees:
        bee_on_flower = False
        bee_x, bee_y, _, _, _,_ = bee
        for flower in flowers:
            flower_x, flower_y, flower_radius, _, _ = flower
            distance = math.sqrt((bee_x - flower_x)**2 + (bee_y - flower_y)**2)
            if distance <= (flower_radius*1.2):
                bee[5] += 1  # Increment the frame count for this bee on this flower
                bee_on_flower = True
                # If the frame counter is less than the threshold, append 0 (no pollination).
                if bee[5] < frame_threshold:
                    valid_bees.append(0)
                # If the frame counter is greater than the threshold,, append 1 (pollination).
                if bee[5] >= frame_threshold:
                    valid_bees.append(1)
                break
        if bee_on_flower == False: # If we go through all the flowers and there is no association with a flower, mark as 0. 
            valid_bees.append(0) # Not on a flower.
    return valid_bees



# # Load the configuration
# config = load_config()

# # Extract the parameters from the config
# bee_model_path = config['bee_model']
# flower_model_path = config['flower_model']
# frame_threshold = config['frame_threshold']
# max_distance = config['max_distance']
# bee_threshold = config['bee_threshold']
# flower_threshold = config['flower_threshold']
# video_path = config['input_path']
# video_path_out = config['output_path']

# # csv_output_path = '../data/output/20191123_130028_detection_counts.csv'  # CSV file path for output

# cap = cv2.VideoCapture(video_path)

# ret, frame = cap.read()
# H, W, _ = frame.shape
# # out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc('X','2','6','4'), int(cap.get(cv2.CAP_PROP_FPS)), (W,H))
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


# model = YOLO(bee_model_path)
# flower_model = YOLO(flower_model_path)

# threshold = 0.5
# frame_count = 0  # To keep track of the current frame number
# detection_counts = []  # List to store frame number and detection count

# tracked_bees = []  # Store bee detections and their associated frame counts
# tracked_flower = []

# while ret:
#     frame_count += 1

#     bee_results = model(frame)[0]

#     flower_results = flower_model(frame)[0]

#     new_tracked_bees = []

#     detection_count = 0  # Counter for the number of detections in the current frame

#     for result in bee_results.boxes.data.tolist():
#         x1, y1, x2, y2, score, class_id = result

#         if score > bee_threshold:
#             mid_x = int((x1+x2)/2)
#             mid_y = int((y1+y2)/2)
#             area = int(abs((x1-x2) * (y1-y2)))
#             new_tracked_bees.append([mid_x, mid_y, area, class_id, score, 0])
            
#             # detection_count += 1
#             # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
#             # cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
#             #             cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    
#     tracked_bees = update_tracked_bees(tracked_bees, new_tracked_bees, max_distance)

#     for result in flower_results.boxes.data.tolist():
#         x1, y1, x2, y2, score, class_id = result

#         if score > flower_threshold:
#             mid_x = int((x1+x2)/2)
#             mid_y = int((y1+y2)/2)
#             min_x = x1
#             min_y = y1
#             max_x = x2
#             max_y = y2

#             # Calculate center of the minimum enclosing circle
#             cx = (min_x + max_x) / 2
#             cy = (min_y + max_y) / 2

#             # Calculate radius of the minimum enclosing circle
#             dx = max_x - cx
#             dy = max_y - cy
#             radius = math.sqrt(dx**2 + dy**2) / 2
#             tracked_flower.append([mid_x, mid_y, radius, class_id, score])

#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
#             cv2.putText(frame, flower_results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

#     valid_bees = is_bee_on_flower(tracked_bees, tracked_flower, frame_threshold)

#     # Annotate valid bees
#     for bee in valid_bees:
#         detection_count += 1
#         mid_x, mid_y, area, class_id, confidence, _ = bee
#         x1 = int(mid_x - (area ** 0.5) / 2)
#         y1 = int(mid_y - (area ** 0.5) / 2)
#         x2 = int(mid_x + (area ** 0.5) / 2)
#         y2 = int(mid_y + (area ** 0.5) / 2)
        
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
#         label = f"{model.names[int(class_id)].upper()}"
#         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

#     out.write(frame)
#     ret, frame = cap.read()

# cap.release()
# out.release()
# cv2.destroyAllWindows()