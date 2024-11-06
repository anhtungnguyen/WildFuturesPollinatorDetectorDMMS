# WildFuturesPollinatorDetectorDMMS

## Introduction

WildFuturesPollinatorDetectorDMMS is designed to detect multiple bees in a "Wild Futures” house, monitoring their pollination behaviour. To achieve this, we use deep learning-based object detection for accurate detecting. This README will show you how to use the models to detect bees, flowers, and pollination events from pre-recorded videos.

## Set up to run on Linux OS

### Installation and Dependencies:
#### Software System:
*  Ubuntu 18.04, 20.04, 22.04
*  Ultralytics
*  Python3 + OpenCV version 4.0+
  
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

## Set up to run on Windows OS

### Installation and Dependencies:
#### Software Requirements:
*  Windows 10+
*  Ultralytics
*  Python3 + OpenCV version 4.0+

### Install Python and related packages
To install Python on your Windows operating system, you can follow this [online guide](https://www.digitalocean.com/community/tutorials/install-python-windows-10).

When this is complete, open a command prompt window and enter the following commands:
'''
pip install ultralytics
'''
'''
pip install opencv-python
'''

Now, clone this git repository to your desired destination. You can do this by opening file explorer and navigating to your desired folder, copying the address as text from the address bar, and entering the following command in a command prompt window. Replace the address line below with the address of the folder you have chosen.
'''
cd C:\Users\your_username\path\to\the\chosen_folder
'''
Install git on your Windows PC by following this [guide](https://github.com/git-guides/install-git) for the Windows section. 
Clone this git repo into the current directory by running this command:
'''
git clone https://github.com/anhtungnguyen/WildFuturesPollinatorDetectorDMMS.git
'''

You may set up the configuration of the AI detection models in the config.yaml file the same way as with the Linux OS detailed above. Ensure that the correct models are placed on the path you have chosen.

With your open command prompt session (or in a newly opened window) in the folder you have cloned, navigate to the pollen_jock folder by using the command:
'''
cd WildFuturesPollinatorDetectorDMMS/pollen_jock
'''
You may now run any of the three detection modes below by running the associated command in the command prompt window. 

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