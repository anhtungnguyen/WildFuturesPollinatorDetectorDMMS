import os
import time
import csv  # Import CSV module to write to CSV files

from ultralytics import YOLO

import cv2
import numpy as np

def _decode_DL_results(_results: np.ndarray) -> np.ndarray:
        
    # Extract the classes, confidence scores, and bounding boxes from the results
    _results_cpu = _results[0].boxes.cpu()
    classes = _results_cpu.cls
    conf = _results_cpu.conf
    boxes = _results_cpu.xyxy

    # Create array in the format [xmin, ymin, xmax, ymax, class, confidence]
    detections = np.zeros((len(classes), 6))
    detections[:, 0] = boxes[:, 0]
    detections[:, 1] = boxes[:, 1]
    detections[:, 2] = boxes[:, 2]
    detections[:, 3] = boxes[:, 3]
    detections[:, 4] = classes
    detections[:, 5] = conf

    return detections

def __calculate_cog(_results: np.ndarray) -> np.ndarray:
    
    _insect_detection = np.zeros(shape=(0,5))

    for result in _results:
        mid_x = int((result[0] + result[2])/2)
        mid_y = int((result[1] + result[3])/2)
        area = int(abs((result[0] - result[2])*(result[1] - result[3])))
        _insect_detection = np.vstack([_insect_detection,(mid_x, mid_y, area, result[4], result[5])])

    return _insect_detection

weights_path = '../data/yolov8_models/insects_best_s.pt'
verify_weights_paths = '../data/yolov8_models/insects_best_l.pt'

video_path = '../data/input/20191123_131057.mp4'
video_path_out = '../data/output/20191123_131057_out.mp4'
csv_output_path = '../data/output/20191123_131057_detection_counts.csv'  # CSV file path for output

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()
H, W, _ = frame.shape
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc('X','2','6','4'), int(cap.get(cv2.CAP_PROP_FPS)), (W,H))
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


model = YOLO(weights_path)
verify_model = YOLO(verify_weights_paths)

dl_detection_confidence = 0.2
verification_confidence = 0.5
insect_iou_threshold = 0
tracking_insect_classes = [0]
frame_count = 0  # To keep track of the current frame number
detection_counts = []  # List to store frame number and detection count

while ret:
    frame_count += 1

    results = model(frame)[0]

    # Use the predict method with custom parameters
    # results = model.predict(
    #     source=frame,
    #     conf=dl_detection_confidence,
    #     show=False,
    #     verbose=False,
    #     save=False,
    #     imgsz=(864, 480),
    #     iou=insect_iou_threshold,
    #     classes=tracking_insect_classes
    # )

    # detections = _decode_DL_results(results)
    # processed_detections = __calculate_cog(detections)

    detection_count = 0  # Counter for the number of detections in the current frame

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > dl_detection_confidence:
            # detection_count += 1

            # Calculate the center of the bounding box
            mid_x = int((x1 + x2) / 2)
            mid_y = int((y1 + y2) / 2)

            # Crop the image for verification
            frame_width = frame.shape[1]
            frame_height = frame.shape[0]
            x0_ = max(0, int(mid_x - 160))
            y0_ = max(0, int(mid_y - 160))
            x1_ = min(int(mid_x + 160), frame_width)
            y1_ = min(int(mid_y + 160), frame_height)

            cropped_frame = frame[y0_:y1_, x0_:x1_] 

            # Create a black frame and place the cropped frame in the center
            black_frame = np.zeros((640, 640, 3), np.uint8)
            black_frame[100:100+cropped_frame.shape[0], 100:100+cropped_frame.shape[1]] = cropped_frame

            # Flip the cropped frame (as per your original instructions)
            crop = cv2.flip(black_frame, -1)

            # Run the second model on the cropped frame for verification
            # verification_results = verify_model(crop)[0]
            # for verified_result in verification_results.boxes.data.tolist():
            #     x_1,y_1,x_2,y_2,score_,class_id_ = verified_result

            #     if score_ > verification_confidence:
            #         detection_count += 1
            #         cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            #         cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            #         break

            verification_results = verify_model.predict(
                source=crop,
                conf=verification_confidence,
                show=False,
                verbose=False,
                iou=0,
                classes=[0],
                augment=True,
                imgsz=(640, 640)
            )

            if len(verification_results[0].boxes) > 0:
                detection_count += 1
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # for detection in processed_detections:
    #     mid_x, mid_y, area, class_id, confidence = detection

    #     if confidence > dl_detection_confidence:
    #         detection_count += 1
            
    #         # Draw a circle at the center of the bounding box (CoG)
    #         # cv2.circle(frame, (int(mid_x), int(mid_y)), 5, (0, 0, 255), -1)  # Red dot for the center

    #         # Draw the bounding box (using decoded results)
    #         x1 = int(mid_x - (area ** 0.5) / 2)
    #         y1 = int(mid_y - (area ** 0.5) / 2)
    #         x2 = int(mid_x + (area ** 0.5) / 2)
    #         y2 = int(mid_y + (area ** 0.5) / 2)
            
    #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)  # Green rectangle

    #         # Annotate the class name and confidence on the frame
    #         label = f"{model.names[int(class_id)].upper()}"
    #         # label = f"{model.names[int(class_id)].upper()} {confidence:.2f}"
    #         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

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
