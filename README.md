# Pineberry Pi Dual Edge TPU

## Preq:
- Raspberry Pi 5
- Pineboard Coral Edge TPU HAT (Dual TPU Compatible)
- Raspberry Pi Bookworm - 64 bit
  - Debian 6.6.32-v8+ #1769 aarch64
- Python 3.9.19

#### Pineboards Ref:

https://pineboards.io/blogs/tutorials/how-to-configure-the-google-coral-edge-tpu-on-the-raspberry-pi-5

## Python 3.9.19
https://github.com/sealmindset/EdgeTPU/wiki/Lowering-the-Python-version-on-a-Raspberry-Pi-5

## Walkthrough Steps
Refer to the [Wiki](https://github.com/sealmindset/EdgeTPU/wiki) for the steps for preparing the Raspberry Pi 5 and the Google Coral Dual Edge TPU with a HAT AI by Pineboards

## Configure the Google Dual Coral Edge TPU on the Raspberry Pi 5

Write the recommended RPI 64 image for Pi 5 to a SD Card. 

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

sudo apt-get update
```

#### Install necessary packages:
```
sudo apt-get install cmake libedgetpu1-std devscripts debhelper dkms dh-dkms
```

### Step 4: Install the Gasket Driver
```
git clone https://github.com/google/gasket-driver.git

cd gasket-driver

sudo debuild -us -uc -tc -b

cd ..

sudo dpkg -i gasket-dkms_1.0-18_all.deb
```

### Step 5: Set Up the udev Rule Add a udev rule to manage device permissions:
```
sudo sh -c "echo 'SUBSYSTEM==\"apex\", MODE=\"0777\", GROUP=\"apex\"' >> /etc/udev/rules.d/65-apex.rules"

sudo groupadd apex && sudo adduser $USER apex

sudo reboot
```

### Verify if the driver is loaded using the following command:
```
sudo lspci -nnn
```

Now, verify the permission is set to RWX
```
ls -l /dev/apex_*
```

## Stress Pi
```
sudo apt-get install stress-ng
```
```
stress-ng --cpu 4 --timeout 60s
```

## Test TPU
Verify the TPU's performance and stability underload when performing AI/ML tasks.

Preq: Python 3.9
```
python3 tst_tpu.py
```





