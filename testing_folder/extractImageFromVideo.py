import cv2
import os

# Path to the folder containing videos
video_folder_path = '../data/input/videos'
# Path to save the extracted images
output_image_path = '../data/input/images'

# Ensure the output directory exists
os.makedirs(output_image_path, exist_ok=True)

# Iterate over each video in the folder
for video_name in os.listdir(video_folder_path):

    if video_name.endswith(".mp4") or video_name.endswith(".avi") or video_name.endswith(".mov"):
        video_path = os.path.join(video_folder_path, video_name)
        cap = cv2.VideoCapture(video_path)
        
        frame_count = 0
        image_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Save every 10th frame
            if frame_count % 2 == 0:

                # rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                image_name = f"{os.path.splitext(video_name)[0]}_frame{image_count}.jpg"
                image_path = os.path.join(output_image_path, image_name)
                cv2.imwrite(image_path, frame)
                image_count += 1
            
            frame_count += 1
        
        cap.release()
print("Image extraction complete.")
