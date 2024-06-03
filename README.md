# Pineberry Pi Dual Edge TPU

## bookworm - Debian 12
https://downloads.raspberrypi.com/raspios_full_arm64/images/raspios_full_arm64-2024-03-15/

##buster - Debian 10
https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2020-08-24/

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

In the Raspberry Pi Imager choose - 'Use Custom'. 

## Initial Boot

Remove Python 3.11

```
sudo ./remove_python.sh
```

Install Python 3.9.0

```
sudo ./install_python.sh
```

```
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3
```

```
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python
```

Verify there are no lingering Python 3.11 dependencies

```
sudo python3 chk_py3.11_dep.py
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
Ensure that the HDF5 library is properly installed.

```
find /usr/lib /usr/local/lib -name 'libhdf5*'
```

#### Reinstall h5py:
After installing the HDF5 library, try installing h5py again using pip.

```
pip install h5py
```

## Install TensorFlow
```
pip install tensorflow
```

### Install picamera2
```
sudo apt update && sudo apt install -y python3-picamera2
```
```
pip install matplotlib
```

## Install PyCoral
```
sudo apt-get install python3-pycoral
```




