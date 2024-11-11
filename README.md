# WildFuturesPollinatorDetectorDMMS_clean

This branch contains the minimum necessary files for running the pollination detector on the Raspberry Pi unit.

## Installation
Clone this repository onto your Raspberry Pi. You must have git installed already.

```
git clone -b pi-clean https://github.com/anhtungnguyen/WildFuturesPollinatorDetectorDMMS.git
```

Create a virtual environment in the new directory you have created using:
```
virtualenv myenv
```

Activate the virtal environment:
```
source myenv/bin/activate
```

Install the required dependencies from the requirements.txt:
```
pip install -r requirements.txt
```

## Running the system automatically on boot
On your Raspberry Pi, open a new terminal instance and navigate to '/etc/systemd/system'.
```
cd /etc/systemd/system
```

You will be creating a new service file. Use the command:
```
sudo nano auto_python_script.service
```
This will open a simple text editor window. Enter the following inside the window:
```
[Unit]
Description= Auto Python Script
After=network.target

[Service]
ExecStart = <path to your cloned git repo>/myenv/bin/python3 <path to your cloned git repo>/Detector/piCam.py
WorkingDirectory = <path to your cloned git repo>/Detector/

StandardOutput=inherit
StandardError=inherit
RemainAfterExit=false
User=root
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Use `CTRL+S` to save the file and `CTRL+X` to exit.

Run the following commands to run the script from the git repo.
```
sudo systemctl daemon-reload
sudo systemctl restart auto_python_script.service
```

From now on, the service will run when the Raspberry Pi is booted.
