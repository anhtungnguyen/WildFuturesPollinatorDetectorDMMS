# WildFuturesPollinatorDetectorDMMS

## Introduction

WildFuturesPollinatorDetectorDMMS is designed to detect multiple bee in a "Wild Futures” house, monitoring their pollination behaviour. To achieve this, Polytrack uses a deep learning-based object detection for accurate detecting.

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

## Set up to run on Window OS
