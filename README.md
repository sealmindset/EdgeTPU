# Setup Coral AI PCIe Accelerator on a Raspberry Pi 5

## Install Coral AI PCIe Edge TPU on Raspberry Pi 5
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

## Create a `Dockerfile`

### Dockerfile

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

## Install Docker

```
sudo apt update
sudo apt install docker.io
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

