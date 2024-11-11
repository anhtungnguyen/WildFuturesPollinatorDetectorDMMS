# WildFuturesPollinatorDetectorDMMS

### Note: If you only want the files necessary for running the system on the Raspberry Pi, use the pi_clean branch instead of the main branch.

## Introduction

WildFuturesPollinatorDetectorDMMS is designed to detect multiple bees in a "Wild Futures” house, monitoring their pollination behaviour. To achieve this, we use deep learning-based object detection for accurate detecting. This README will show you how to use the models to detect bees, flowers, and pollination events from pre-recorded videos.
This also covers:
- The steps to replicate the procedure
- The Bill of materials
- Roboflow dataset
- CAD models
- Future steps for scalability
- Recommendations for improvements 

We recommend that you download and install VSCode to run all of the below components. You can download and learn how to use VSCode at this [link](https://code.visualstudio.com/docs).

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
```
pip install ultralytics
```
```
pip install opencv-python
```

Now, clone this git repository to your desired destination. You can do this by opening file explorer and navigating to your desired folder, copying the address as text from the address bar, and entering the following command in a command prompt window. Replace the address line below with the address of the folder you have chosen.
```
cd C:\Users\your_username\path\to\the\chosen_folder
```
Install git on your Windows PC by following this [guide](https://github.com/git-guides/install-git) for the Windows section. 
Clone this git repo into the current directory by running this command:
```
git clone https://github.com/anhtungnguyen/WildFuturesPollinatorDetectorDMMS.git
```

You may set up the configuration of the AI detection models in the config.yaml file the same way as with the Linux OS detailed above. Ensure that the correct models are placed on the path you have chosen.

With your open command prompt session (or in a newly opened window) in the folder you have cloned, navigate to the pollen_jock folder by using the command:
```
cd WildFuturesPollinatorDetectorDMMS/pollen_jock
```
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
## Bill of Materials
| Item                            | Link                                                                                                 |
|---------------------------------|------------------------------------------------------------------------------------------------------|
| Raspberry Pi 5                  | https://raspberry.piaustralia.com.au/products/raspberry-pi-5?variant=44207825649888                  |
| Micro SD card (256 GB)          | https://www.jbhifi.com.au/products/samsung-pro-ultimate-256gb-micro-sd-card                          |
| Hailo AI kit                    | https://raspberry.piaustralia.com.au/products/raspberry-pi-ai-kit                                    |
| Battery pack                    | https://core-electronics.com.au/raspberry-pi-5-18650-battery-ups-hat-51v-5a.html                     |
| 4x 18650 batteries              | https://core-electronics.com.au/polymer-lithium-ion-battery-18650-cell-2600mah.html                  |
| Pi cam module 3                 | https://core-electronics.com.au/raspberry-pi-camera-3.html                                           |
| 3D printed parts                | N/A                                                                                                  |
| Heatsink+Fan for Raspberry Pi 5 | https://raspberry.piaustralia.com.au/products/raspberry-pi-active-cooler?_pos=1&_sid=40905f3a8&_ss=r |
| Raspberry Pi Mini Ribbon Cable  | https://raspberry.piaustralia.com.au/products/raspberry-pi-display-cable-standard-mini               |
| Waterproof case                 | https://www.amazon.com.au/Wutusent-Dustproof-Waterproof-Universal-Electrical/dp/B0BZMC1MNG?th=1      |

## CAD files
Included in the CAD files folder is both the solid works parts and the printable STL files. Currently it is designed to print with PLA but its recommended to use an alternate filament capable of withstanding the UV rays from the sun. 

## AI Models
The models were initially trained with a separate dataset for bees and flowers, these have now been merged so that there is a separate class. The dataset can be found below:
[Not the Bees Dataset](https://universe.roboflow.com/wild-futures-pollinator-detector/not-the-bees/dataset/11)
The objective was to train both on bees and flowers that are currently blooming and have been augmented along with the usage of 200 epochs. This pre-trained model can be found in Not The Bees Dataset.zip

Instructions on how to train with YOLOv8 on your own dataset is included here:
[Train - Ultralytics YOLO Docs](https://docs.ultralytics.com/modes/train/#introduction)
A graphics card with CUDA cores is recommended.
You will also need pytorch:
[Start Locally | PyTorch](https://pytorch.org/get-started/locally/)


## Scalability Analysis & Future improvements
Under the assumption that this would be implemented to hundreds of planter boxes, it would almost certainly be more efficient to not use a raspberry pi. Instead, what could be done is by using a supply of cheap cameras connected to a google nest in leu of a series of raspberry pi cameras. From there, the information needs to be processed by AI, there are two routes: one piping the information to a workstation computer for AI processing and another one to a cloud server. There are benefits and drawbacks with each solution as the workstation would grow more expensive in proportion to the number of cameras but could also be utilised in conjunction with other projects, whilst the cloud server could be easily upscaled to accommodate with any number of cameras but has concurrent and ongoing costs. These cameras could instead also be powered by routed by cables attached to mains power which can also be used to power other projects (i.e. irrigation system). 
Future improvements are mainly based off the quality of the model and dataset which would largely improve the accuracy and reliability of the pollinator detection, other than this the following features can also be added. The mounting procedure would fair better upscaled if instead of using 3D printed mount, the use of dedicated screws for cameras to the structure would serve as a more permanent solution. 
- Path tracking for pollinators 
- Information dashboard for mass display of data, this can also potentially be integrated with the irrigation project information.
- Individual pollinator species identification 
- Detection of the status of the flower (i.e. either flowering, blooming, wilting) 
- Record per flower of what has pollinated it and from what flower:
Example:
**Hibbertia Flower 32** has been pollinated by **Hoverfly 4** which has **Hibbertia Flower 14** pollen
**Hibbertia Flower 32** has been pollinated by **Hoverfly 1** which has **Hibbertia Flower 54** pollen
- On demand real time video streaming with annotated frames
- Ordered video and file storage.
- Big data integration with assumption of multiple structures so that an analysis of entire neighbourhoods or cities can be made
Some of the features require a stronger workstation/access to cloud storage as it is unlikely a raspberry pi 5 with an AI kit is sufficient alone. 

