# Pineberry Pi Dual Edge TPU

## Preq:
- Raspberry Pi 5
- Pineboard Coral Edge TPU HAT (Dual TPU Compatible)
- Raspberry Pi Bookworm - 64 bit
- Debian 1:6.6.31-1+rpt1 aarch64
- Python 3.11.2

#### Pineboards Ref:

https://pineboards.io/blogs/tutorials/how-to-configure-the-google-coral-edge-tpu-on-the-raspberry-pi-5

#### Yolov8 Ref:

https://dagshub.com/Ultralytics/ultralytics/pulls/6583/files?page=0&path=docs%2Fen%2Fguides%2Fraspberry-pi.md

## Configure the Google Dual Coral Edge TPU on the Raspberry Pi 5
### Download the image locally

https://www.raspberrypi.com/software/operating-systems/

### Choose 'Use Custom' from the RPI Imager

Write the RPI image to a SD Card. 

## Initial Boot
### Configure Hardware Settings
#### Step 1: Configure Hardware Settings

```
sudo sed -i '/\[all\]/a # Enable the PCIe External connector.\ndtparam=pciex1\nkernel=kernel8.img\n# Enable Pineboards Hat Ai\ndtoverlay=pineboards-hat-ai' /boot/firmware/config.txt
```

#### Step 2: Update the Kernel

```
sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y && apt autoremove -y
```

Allow pip without parameter
```
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

```
sudo reboot
```

### Step 3: Install the PCIe Driver and Edge TPU Runtime
```
sudo apt update
```

#### Add the Google Coral Edge TPU package repository:
```
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
```

#### Import the repository GPG key:
```
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

```
sudo apt-get update
```

#### Install necessary packages:
```
sudo apt-get install cmake libedgetpu1-std devscripts debhelper dkms dh-dkms
```

### Step 4: Install the Gasket Driver
```
git clone https://github.com/google/gasket-driver.git
```

```
cd gasket-driver
```

```
sudo debuild -us -uc -tc -b
```

```
cd ..
```

```
sudo dpkg -i gasket-dkms_1.0-18_all.deb
```

### Step 5: Set Up the udev Rule Add a udev rule to manage device permissions:
```
sudo sh -c "echo 'SUBSYSTEM==\"apex\", MODE=\"0660\", GROUP=\"apex\"' >> /etc/udev/rules.d/65-apex.rules"
```

```
sudo groupadd apex && sudo adduser $USER apex
```

```
sudo reboot
```

### Verify if the driver is loaded using the following command:
```
sudo lspci -v
```

```
ls /dev/apex_*
```

## Yolo v8

### Install Necessary Packages

#### Update the Raspberry Pi:

```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get autoremove -y
```

#### Install the ultralytics Python package:

```
pip3 install ultralytics
```
```
sudo reboot
```

#### Initiate TCP Stream with Libcamera
##### Start the TCP stream:
```
libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888
```

##### Perform YOLOv8 Inference

To perform inference with YOLOv8, you can use the following Python code snippet:

```
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model('tcp://127.0.0.1:8888', stream=True)

while True:
    for result in results:
        boxes = result.boxes
        probs = result.probs
```





