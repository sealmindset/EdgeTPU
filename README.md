# Pineberry Pi Dual Edge TPU

https://downloads.raspberrypi.com/raspios_full_arm64/images/raspios_full_arm64-2024-03-15/

https://pineboards.io/pages/documentation-hat-ai-dual

https://coral.ai/docs/notes/build-coral/

https://www.youtube.com/watch?v=3YqbO2AlepM

https://github.com/freedomwebtech/tflite-custom-object-bookworm

https://jamesjdavis.medium.com/how-to-update-raspberry-pi-just-follow-these-easy-steps-ac507cf70238#c1e2

https://dataslayer.notion.site/Setup-Coral-AI-PCIe-Accelerator-on-a-Raspberry-Pi-5-use-it-with-Frigate-and-PyCoral-68bf94868cf84731860318e52c9c398a

https://www.youtube.com/watch?v=QmUJOFHr-No

## Image the lastest RPI distro
Create a image to a SD Card. Download it locally.

```
wget -c https://downloads.raspberrypi.com/raspios_full_arm64/images/raspios_full_arm64-2024-03-15/2024-03-15-raspios-bookworm-arm64-full.img.xz
```

In the Raspberry Pi Imager choose - 'Use Custom'

```
sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
```

## Upgrade to the lastest distro

```
sudo apt update && sudo apt dist-upgrade -y && sudo apt clean -y

```

#### Reboot
```
sudo reboot
```

### Update

```
sudo rpi-update
```

## Python 3.9.0
### Dependencies
Make sure you have all necessary dependencies installed:
```
sudo apt update
```
```
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev tar wget vim
```

### Download Python 3.9.0
Download the source code and extract Python 3.9.0
```
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
```
```
tar -xvf Python-3.7.9.tgz
```
```
cd Python-3.9.0/
```
### Configure
```
./configure --enable-optimizations
```
```
make -j 4  # Use the number of cores you have
```
```
sudo make altinstall
```
### Set the New Python Version as Default:
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1
sudo update-alternatives --config python3
```

### remove the req to add --break-system-packages

```
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

### opencv-python
```
sudo pip install opencv-python
```


### install mediapipe
```
sudo pip install mediapipe
```

## Test
```
python txt_detect.py --recordduration 60
```

## TensorFlow

### Install HDF5 Library:

```
sudo apt-get update && sudo apt-get install libhdf5-dev
```

### Test HDF5
Ensure that the HDF5 library is properly installed. You can verify this by checking if the libhdf5.so file is present in your library directories.

```
find /usr/lib /usr/local/lib -name 'libhdf5*'
```

#### Reinstall h5py:
After installing the HDF5 library, try installing h5py again using pip.

```
ssh pip install h5py
```

##### Set Environment Variables (if necessary):
If the library is installed but not found, you might need to set the HDF5_DIR environment variable to the location of the HDF5 installation.

```
export HDF5_DIR=/usr/local/hdf5
```

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/hdf5/lib
```

## Install TensorFlow
```
sudo pip install tensorflow
```

### Install picamera2
```
sudo apt update
```
```
sudo apt install -y python3-picamera2
```
```
sudo pip install matplotlib
```






