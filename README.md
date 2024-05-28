# Coral AI PCIe Edge TPU on Pineberry for a RPi 5

Carefully, install the board to the Pi. 

## Enable Pineberry Board

```
sudo vi /boot/firmware/config.txt
```

Add the following lines to the file:

```
[all]
# Enable the PCIe External connector.
dtparam=pciex1
kernel=kernel8.img
# Enable Pineboards Hat Ai
dtoverlay=pineboards-hat-ai
```

Reboot

REF: https://pineboards.io/blogs/tutorials/how-to-configure-the-google-coral-edge-tpu-on-the-raspberry-pi-5

## Install Coral Drivers
Execute the scripts below to install the drivers and tweak the OS. After each install, it will reboot.

NOTE: TODO - combine all 3 into one

### coralInstall1

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall1.sh?token=GHSAT0AAAAAACSETBXD7HJN6OEZMKUBWTMAZSVG76A | sh
```

### coralInstall2

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall3.sh?token=GHSAT0AAAAAACSETBXC3UKAL6AQV74CWGKSZSVHC7Q | sh
```

### coralInstall3

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall1.sh?token=GHSAT0AAAAAACSETBXD7HJN6OEZMKUBWTMAZSVG76A | sh
```

## Verify the TPU is accessible

```
python verifyTPU.py
```

## Test Coral to see if it works

```
python testCoral.py
```

There are two approach that can be taken, the first option is to run py-env in order to use Python 3.9, the second is to run within Docker.

### Once rebooted, verify that the accelerator module is detected:

```
lspci -nn | grep 089a
```

You should see something like this:

```
03:00.0 System peripheral: Device 1ac1:089a
```

## Give permissions to the /dev/apex_0 device 

### creating a new udev rule:
Open a terminal and use your favorite text editor with sudo to create a new file in /etc/udev/rules.d/. The file name should end with .rules. It's common practice to start custom rules with a higher number (e.g., 99-) to ensure they are applied after the default rules. For example:

```
sudo vi /etc/udev/rules.d/101-coral-edgetpu.rules
```

#### Add a rule to the file:

You'll need to identify your device by attributes like idVendor and idProduct or use the KERNEL attribute if the device path is consistent. For the Coral Edge TPU, using the device path /dev/apex_0 directly in a udev rule is not standard because this path might not be persistent across reboots or other device changes. Instead, use attributes to match the device.

However, since we're dealing with a specific device path here, your rule might look something like this, assuming /dev/apex_0 is consistently named and you're setting permissions:

```
KERNEL=="apex_0", MODE="0666"
```

This rule sets the device file /dev/apex_0 to be readable and writable by everyone. Adjust the MODE as necessary for your security requirements.

Reload the udev rules and trigger them: After saving the file, you need to reload the udev rules and trigger them to apply the changes without rebooting. Reload the rules:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

#### Verify /dev/apex_0 and MSI-X are enabled:

Verify that the permissions for /dev/apex_0 are set as expected. After rebooting, check the permissions of the device file:

```
ls -l /dev/apex_0
```

Also verify all Message Signaled Interrupts (MSI) are enabled:

```
sudo lspci -vvv|grep -i MSI-X
```

You should see something like this, where + indicates that MSI-X is enabled and - indicates that it's disabled:

```
Capabilities: [d0] MSI-X: Enable+ Count=128 Masked-
Capabilities: [b0] MSI-X: Enable+ Count=61 Masked-
```

REF: https://gist.github.com/lpaolini/8652a54a36ec6b446aba18a7f483ac0b

## Docker

```
sudo apt update
sudo apt install docker.io
```

### Create a `Dockerfile`

##### Dockerfile

```
FROM debian:10

WORKDIR /home
ENV HOME /home
RUN cd ~
RUN apt-get update
RUN apt-get install -y git nano python3-pip python-dev pkg-config wget usbutils curl

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
| tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update
RUN apt-get install -y edgetpu-examples
```

### Verify Docker is working



#### Become root

```
sudo sudo -s
```

#### Check docker

```
docker ps -a
```

### Build and tag docker image

```
docker build -t "coral" .
```

### Run and enter container

```
docker run -it --device /dev/apex_0:/dev/apex_0 coral /bin/bash
```

```
python3 /usr/share/edgetpu/examples/classify_image.py --model /usr/share/edgetpu/examples/models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --label /usr/share/edgetpu/examples/models/inat_bird_labels.txt --image /usr/share/edgetpu/examples/images/bird.bmp
```

## Data Slayer

https://dataslayer.notion.site/Setup-Coral-AI-PCIe-Accelerator-on-a-Raspberry-Pi-5-use-it-with-Frigate-and-PyCoral-68bf94868cf84731860318e52c9c398a

https://gist.github.com/dataslayermedia

https://github.com/dataslayermedia?tab=repositories

## Verify Camera is working

```
rpicam-hello -n --timeout 20
```

#### Reference

https://www.raspberrypi.com/documentation/computers/camera_software.html#building-rpicam-apps-without-building-libcamera

