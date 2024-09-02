# -*- coding: utf-8 -*-
"""Train_YOLOv8_crates/bottles_dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18EZzwTebmJcaZi60oHtRlI-vddd32cHc
"""

### 1. Mount Google Drive ###

from google.colab import drive

drive.mount('/content/gdrive')

### 2. Define root directory ###

ROOT_DIR = '/content/gdrive/My Drive/training_model'

### 3. Install Ultralytics ###

!pip install ultralytics

### 4. Train model ###

import os

from ultralytics import YOLO


# Load a model
model = YOLO("yolov8n.pt")  # load pre trained model

# Use the model
results = model.train(data=os.path.join(ROOT_DIR, "google_colab_config.yaml"), epochs=86)  # train the model

### 5. Copy results ###
import shutil
import os

# Define the source directory (your training results)
source_dir = '/content/runs'

# Define the destination directory on your Google Drive
destination_dir = '/content/gdrive/My Drive/training_model'

# Check if the destination directory exists; create it if it doesn't
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Use shutil to copy the entire directory contents to Google Drive
for src_dir, dirs, files in os.walk(source_dir):
    dst_dir = src_dir.replace(source_dir, destination_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)  # Optionally remove the file if it already exists in the destination to avoid errors
        shutil.copy(src_file, dst_dir)

# !cp -r /content/runs '/content/gdrive/My Drive/tranining_model'