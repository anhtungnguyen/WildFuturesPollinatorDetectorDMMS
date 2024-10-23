# WildFuturesPollinatorDetectorDMMS

## Introduction

WildFuturesPollinatorDetectorDMMS is designed to detect multiple bee in a "Wild Futures” house, monitoring their pollination behaviour. To achieve this, Polytrack uses a deep learning-based object detection for accurate detecting.

## Set up to run on Pi OS

### Installation and Dependencies:
#### Software System:
*  Pi OS
*  Ultralytics
*  Python3 + OpenCV version 4.0+
### Hardware System:
*  Raspberry Pi 5 with micro SD card (> 64 GB) 
*  Hailo AI kit

To install and setup a new Raspberry Pi with Pi OS, please follow this [link](https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system)

Clone the repo:
```
git clone git@github.com:anhtungnguyen/WildFuturesPollinatorDetectorDMMS.git
```

Pollen_jock utilizes OpenCV for image processing and Ultralytics YOLOv8 for deep learning-based object detection. Dependencies related to this code are provided in the requirements.txt and environment_dmms.yml files.

#### Training YOLOv8 Object detection model

Pollen_jock uses a YOLOv8 object detection model to accurately detect bee and flowers in videos. It offers the option to use separate YOLOv8 models for bee and flower detection, enabling the use of existing annotated datasets. For more information on training YOLOv8 models, please refer to the YOLOv8 tutorials below.

* [How to Train YOLOv8 Object Detection on a Custom Dataset](https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/)
* [Model Training with Ultralytics YOLO](https://docs.ultralytics.com/modes/train/)

Alternatively, you can download a pre-trained YOLOv8 model for detecting bee and flower [here](https://drive.google.com/drive/u/0/folders/1ruobLQXmKmgotj4ko5wrACg6ftf_-6o0). This model is associated with the datasets [bee](https://universe.roboflow.com/wild-futures-pollinator-detector/not-the-bees/dataset/8) and [flower]()

### Configuration file
To edit configuration file, open the file config.yaml in WildFuturesPollinatorDetectorDMMS/pollen_jock folder

* bee_model: path to bee detection model

* flower_model: path to flower detection model

* frame_threshold: number of consecutive frame checking if the bee remains on the flower

* max_distance: max distance to considered the same bee between 2 consecutive frame

* bee_threshold: confidence for bee detection model

* flower_threshold: confidence for flower detection model

* input_path: input video source

* output_path: output video source

### Run the program

Navigate to the repo

```
cd WildFuturesPollinatorDetectorDMMS/pollen_jock
```

##### Bee detection only mode
```
python3 testDetectionOnly.py
```

##### Flower detection only mode
```
python3 testFlowerModel.py
```

##### Pollinated bee detection mode
```
python3 testPollinatorOnFlower.py
```

### To set up Auto-Run program(s) on Boot

#### Using systemd Service

1. Creating a systemd service gives you more control over the execution of your program.
```
sudo nano /etc/systemd/system/my_program.service
```
2. Add the following content to the file:
```
[Unit]
Description=My Program

[Service]
ExecStart=/usr/bin/python3 /home/pi/your_script.py
WorkingDirectory=/home/pi/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
Replace /home/pi/your_script.py with the full path to your script.

3. Save and exit the editor.
  
4. Enable the service so it runs on boot:
```
sudo systemctl enable my_program.service
```
5. Start the service immediately (optional):
```
sudo systemctl start my_program.service
```
