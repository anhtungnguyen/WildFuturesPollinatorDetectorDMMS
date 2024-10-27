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

## Conversion from YOLOv8 .pt to HAILO .hef

### Note: The primary guide was followed using wsl2.

### What is this? 

The HAILO Dataflow Compiler is a tool used to convert computer vision models from a variety of formats (YOLO versions, ResNet, Tensorflow, etc.) into a single format which can be read by HAILO hardware which is integrated on the Raspberry Pi AI Kit. It converts the model into an optimised format to run at as high a frame rate as possible. Note that this library can only be run on Linux software.

### How to Use it? 
The primary tutorial being followed is here. It describes downloading, installation and running of the DFC: 
* [Tutorial of AI Kit with Raspberry Pi 5 about YOLOv8n object detection](https://wiki.seeedstudio.com/tutorial_of_ai_kit_with_raspberrypi5_about_yolov8n_object_detection/)

  * It is recommended to not use the command line that this tutorial guide uses to convert the models to different file formats due to the clumsiness of the arguments provided and inexperience.
  * Instead, after installing the Hailo DFC, navigate to the hailo/lib/python3.<version>/site-packages/hailo_tutorials/notebooks folder and work through tutorials 1-3 to produce a .hef file. Note that a .onnx file is needed before starting.

* Importantly, successful running of the DFC depends on the computer having enough RAM.
  * During my run of the DFC, RAM usage peaked at 26 GB.
  * Recommended specs are 32 GB, and minimum is 16 GB (likely won’t cut it for complex YOLO models).

* When asked to specify the end-nodes for the input .onnx model, refer to the hailo_model_zoo/hailo_model_zoo/cfg/networks folder and find the corresponding .yaml file for your starting pre-trained model, e.g. yolov8n.yaml
  * Copy in the end-nodes in the .yaml folder.
  * You must have downloaded the hailo model zoo for this.
  * If you have custom-trained your own network from scratch, you may need to know your end-nodes yourself.
* Each step is independently short, save for compilation. On the yolov8n model for bee detection this took up to 1 and a half hours when targeting maximum performance. 

### How to get a .onnx file
To obtain a .onnx file from a .pt file, run the following command using the ultralytics python library: 
* yolo export model<model_name> imgsz=640 format=onnx opset=11

### Troubleshooting links 
Some useful community posts which were used in troubleshooting (login may be required): 
* https://community.hailo.ai/t/unable-to-compile-quantized-har-file-to-hef-for-yolov8n-model/2672
* https://community.hailo.ai/t/compilation-of-yolov8-network/2028/11
* https://community.hailo.ai/t/how-to-install-the-hailo-dataflow-compiler-dfc-on-wsl2/2890

 
