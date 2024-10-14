# import os
# import time
# import csv  # Import CSV module to write to CSV files
# import math

# from ultralytics import YOLO

# import cv2
# import numpy as np

# def _decode_DL_results(_results: np.ndarray) -> np.ndarray:
        
#     # Extract the classes, confidence scores, and bounding boxes from the results
#     _results_cpu = _results[0].boxes.cpu()
#     classes = _results_cpu.cls
#     conf = _results_cpu.conf
#     boxes = _results_cpu.xyxy

#     # Create array in the format [xmin, ymin, xmax, ymax, class, confidence]
#     detections = np.zeros((len(classes), 6))
#     detections[:, 0] = boxes[:, 0]
#     detections[:, 1] = boxes[:, 1]
#     detections[:, 2] = boxes[:, 2]
#     detections[:, 3] = boxes[:, 3]
#     detections[:, 4] = classes
#     detections[:, 5] = conf

#     return detections

# def __calculate_cog(_results: np.ndarray) -> np.ndarray:
    
#     _insect_detection = np.zeros(shape=(0,5))

#     for result in _results:
#         mid_x = int((result[0] + result[2])/2)
#         mid_y = int((result[1] + result[3])/2)
#         area = int(abs((result[0] - result[2])*(result[1] - result[3])))
#         _insect_detection = np.vstack([_insect_detection,(mid_x, mid_y, area, result[4], result[5])])

#     return _insect_detection

# def _decode_flower_detections(_results: np.ndarray) -> np.ndarray:
    
#     # Extract the classes, confidence scores, and bounding boxes from the results
#     _results_cpu = _results[0].boxes.cpu()
#     classes = _results_cpu.cls
#     conf = _results_cpu.conf
#     boxes = _results_cpu.xyxy

#     # Create array in the format [xmin, ymin, xmax, ymax, class, confidence]
#     detections = np.zeros((len(classes), 6))
#     detections[:, 0] = boxes[:, 0]
#     detections[:, 1] = boxes[:, 1]
#     detections[:, 2] = boxes[:, 2]
#     detections[:, 3] = boxes[:, 3]
#     detections[:, 4] = classes
#     detections[:, 5] = conf

#     return detections

# def __calculate_flower_cog(_results: np.ndarray) -> np.ndarray:
    
#     _flower_detection = np.zeros(shape=(0,5))

#     for result in _results:
#         min_x = result[0]
#         min_y = result[1]
#         max_x = result[2]
#         max_y = result[3]

#         # Calculate center of the minimum enclosing circle
#         cx = (min_x + max_x) / 2
#         cy = (min_y + max_y) / 2

#         # Calculate radius of the minimum enclosing circle
#         dx = max_x - cx
#         dy = max_y - cy
#         radius = math.sqrt(dx**2 + dy**2) / 2

#         _flower_detection = np.vstack([_flower_detection,(cx, cy, radius, result[4], result[5])])

#     return _flower_detection

# # Function to check if a bee is on a flower for at least 1 second
# def is_bee_on_flower(bees, flowers, frame_threshold=30):
#     valid_bees = []
#     for bee in bees:
#         bee_x, bee_y, _, _, _,_ = bee
#         for flower in flowers:
#             flower_x, flower_y, flower_radius, _, _ = flower
#             distance = math.sqrt((bee_x - flower_x)**2 + (bee_y - flower_y)**2)
#             if distance <= flower_radius:
#                 bee[5] += 1  # Increment the frame count for this bee on this flower
#                 if bee[5] >= frame_threshold:
#                     valid_bees.append(bee)
#                 break
#     return valid_bees

# weights_path = '../data/yolov8_models/lastest_bee.pt'
# verify_weights_paths = '../data/yolov8_models/insects_best_l.pt'
# flower_weight_path = '../data/yolov8_models/latest_flower.pt'

# video_path = '../data/input/videos/5126-4046-4b56-8307-07ad3eb4d61b.mp4'
# video_path_out = '../data/output/5126-4046-4b56-8307-07ad3eb4d61b_out.mp4'
# # csv_output_path = '../data/output/20191123_131057_detection_counts.csv'  # CSV file path for output

# cap = cv2.VideoCapture(video_path)

# ret, frame = cap.read()
# H, W, _ = frame.shape
# # out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc('X','2','6','4'), int(cap.get(cv2.CAP_PROP_FPS)), (W,H))
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


# model = YOLO(weights_path)
# verification_model = YOLO(verify_weights_paths)
# flower_model = YOLO(flower_weight_path)

# dl_detection_confidence = 0.5
# verification_confidence = 0.5
# insect_iou_threshold = 0
# tracking_insect_classes = [0]
# frame_count = 0  # To keep track of the current frame number
# detection_counts = []  # List to store frame number and detection count

# flower_detection_confidence = 0.05
# flower_iou_threshold = 0.5
# flower_classes = [0]

# # Keep track of bees and flowers across frames
# tracked_bees = []  # Store bee detections and their associated frame counts

# while ret:
#     frame_count += 1

#     # results = model(frame)[0]

#     # Use the predict method with custom parameters
#     results = model.predict(
#         source=frame,
#         conf=dl_detection_confidence,
#         show=False,
#         verbose=False,
#         save=False,
#         imgsz=(864, 480),
#         iou=insect_iou_threshold,
#         classes=tracking_insect_classes
#     )

#     detections = _decode_DL_results(results)
#     processed_detections = __calculate_cog(detections)

#     # Flower
#     flowers_results = flower_model.predict(source=frame, 
#                                     conf=flower_detection_confidence, 
#                                     show=False, 
#                                     verbose = False, 
#                                     iou = flower_iou_threshold, 
#                                     classes = flower_classes)
        
#     flowers_detections = _decode_flower_detections(flowers_results)
#     flowers_processed_detections = __calculate_flower_cog(flowers_detections)

#     detection_count = 0  # Counter for the number of detections in the current frame

#     # for result in results.boxes.data.tolist():
#     #     x1, y1, x2, y2, score, class_id = result

#     #     if score > dl_detection_confidence:
#     #         detection_count += 1
#     #         cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
#     #         cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
#     #                     cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

#     for detection in processed_detections:
#         mid_x, mid_y, area, class_id, confidence = detection

#         # if confidence > dl_detection_confidence:
#         #     # detection_count += 1
            
#         #     # Crop the image for verification
#         #     frame_width = frame.shape[1]
#         #     frame_height = frame.shape[0]
#         #     x0 = max(0, int(mid_x - 160))
#         #     y0 = max(0, int(mid_y - 160))
#         #     x1 = min(int(mid_x + 160), frame_width)
#         #     y1 = min(int(mid_y + 160), frame_height)

#         #     cropped_frame = frame[y0:y1, x0:x1]

#         #     # Create a black frame and place the cropped frame in the center
#         #     black_frame = np.zeros((640, 640, 3), np.uint8)
#         #     black_frame[100:100+cropped_frame.shape[0], 100:100+cropped_frame.shape[1]] = cropped_frame

#         #     # Flip the cropped frame (as per your original instructions)
#         #     crop = cv2.flip(black_frame, -1)

#         #     # Run the second model on the cropped frame
#         #     verification_results = verification_model.predict(
#         #         source=crop,
#         #         conf=verification_confidence,
#         #         show=False,
#         #         verbose=False,
#         #         iou=0,
#         #         classes=[0],
#         #         augment=True,
#         #         imgsz=(640, 640)
#         #     )

#         #     if len(verification_results[0].boxes) > 0:
#         tracked_bees.append([mid_x, mid_y, area, class_id, confidence, 0])
#                 # # If the second model verifies the detection, annotate it
#                 # detection_count += 1
#                 # # Draw the bounding box (using decoded results)
#                 # x1 = int(mid_x - (area ** 0.5) / 2)
#                 # y1 = int(mid_y - (area ** 0.5) / 2)
#                 # x2 = int(mid_x + (area ** 0.5) / 2)
#                 # y2 = int(mid_y + (area ** 0.5) / 2)
            
#                 # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)  # Green rectangle

#                 # # Annotate the class name and confidence on the frame
#                 # label = f"{model.names[int(class_id)].upper()}"
#                 # # label = f"{model.names[int(class_id)].upper()} {confidence:.2f}"
#                 # cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

#     # Filter out bees that are not on flowers long enough
#     valid_bees = is_bee_on_flower(tracked_bees, flowers_processed_detections)

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

#     # Append the frame number and detection count to the list
#     detection_counts.append([frame_count, detection_count])

#     # Write to CSV file every 10 frames
#     # if frame_count % 10 == 0:
#     #     with open(csv_output_path, mode='a', newline='') as file:
#     #         writer = csv.writer(file)
#     #         if frame_count == 10:  # Write the header only once
#     #             writer.writerow(['Frame Number', 'Detection Count'])
#     #         writer.writerows(detection_counts)
#     #     detection_counts = []  # Clear the list after writing to the file

#     out.write(frame)
#     ret, frame = cap.read()

# cap.release()
# out.release()
# cv2.destroyAllWindows()

# # Write any remaining detection counts to the CSV file after the loop ends
# # if detection_counts:
# #     with open(csv_output_path, mode='a', newline='') as file:
# #         writer = csv.writer(file)
# #         writer.writerows(detection_counts)


import os
import time
import csv  # Import CSV module to write to CSV files

from ultralytics import YOLO

import cv2
import numpy as np
import copy
from copy import deepcopy
import math

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
        bee_x, bee_y, _, _, _,_ = bee
        for flower in flowers:
            flower_x, flower_y, flower_radius, _, _ = flower
            distance = math.sqrt((bee_x - flower_x)**2 + (bee_y - flower_y)**2)
            if distance <= flower_radius:
                bee[5] += 1  # Increment the frame count for this bee on this flower
                if bee[5] >= frame_threshold:
                    valid_bees.append(bee)
                break
    return valid_bees

# weights_path = '../data/yolov8_models/insects_best_s.pt'
weights_path = '../data/yolov8_models/lastest_bee.pt'
classification_path = '../data/yolov8_models/classification_new.pt'
flower_path = '../data/yolov8_models/pollen_jock_flowers.pt'

video_path = '../data/input/videos/20241001_120405.mp4'
video_path_out = '../data/output/20241001_120405_out_t.mp4'
# csv_output_path = '../data/output/20191123_130028_detection_counts.csv'  # CSV file path for output

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()
H, W, _ = frame.shape
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc('X','2','6','4'), int(cap.get(cv2.CAP_PROP_FPS)), (W,H))
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


model = YOLO(weights_path)
classification_model = YOLO(classification_path)
flower_model = YOLO(flower_path)

threshold = 0.5
classification_threshold = 0.5
frame_count = 0  # To keep track of the current frame number
detection_counts = []  # List to store frame number and detection count

tracked_bees = []  # Store bee detections and their associated frame counts
tracked_flower = []

while ret:
    frame_count += 1

    results = model(frame)[0]

    flower_results = flower_model(frame)[0]

    new_tracked_bees = []

    detection_count = 0  # Counter for the number of detections in the current frame

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            mid_x = int((x1+x2)/2)
            mid_y = int((y1+y2)/2)
            area = int(abs((x1-x2) * (y1-y2)))
            new_tracked_bees.append([mid_x, mid_y, area, class_id, score, 0])
            
            # detection_count += 1
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            # cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    
    tracked_bees = update_tracked_bees(tracked_bees, new_tracked_bees)

    for result in flower_results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            mid_x = int((x1+x2)/2)
            mid_y = int((y1+y2)/2)
            min_x = x1
            min_y = y1
            max_x = x2
            max_y = y2

            # Calculate center of the minimum enclosing circle
            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2

            # Calculate radius of the minimum enclosing circle
            dx = max_x - cx
            dy = max_y - cy
            radius = math.sqrt(dx**2 + dy**2) / 2
            tracked_flower.append([mid_x, mid_y, radius, class_id, score])

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, flower_results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    valid_bees = is_bee_on_flower(tracked_bees, tracked_flower)

    # Annotate valid bees
    for bee in valid_bees:
        detection_count += 1
        mid_x, mid_y, area, class_id, confidence, _ = bee
        x1 = int(mid_x - (area ** 0.5) / 2)
        y1 = int(mid_y - (area ** 0.5) / 2)
        x2 = int(mid_x + (area ** 0.5) / 2)
        y2 = int(mid_y + (area ** 0.5) / 2)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        label = f"{model.names[int(class_id)].upper()}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()