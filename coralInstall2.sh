#!/bin/bash

cd /

sudo apt update
sudo apt upgrade -y
sudo apt install devscripts debhelper dkms -y

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update


sudo apt-get install libedgetpu1-std

sudo apt install -y devscripts debhelper

sudo apt-get install dh-dkms

# Clone the Gasket driver repository
sudo git clone https://github.com/google/gasket-driver.git

# Change directory to the cloned repository
cd gasket-driver

# Build the Gasket driver package
sudo debuild -us -uc -tc -b

# Go back to the parent directory
cd ..

# Install the built Gasket driver package
sudo dpkg -i gasket-dkms_1.0-18_all.deb


sudo sh -c "echo 'SUBSYSTEM==\"apex\", MODE=\"0660\", GROUP=\"apex\"' >> /etc/udev/rules.d/65-apex.rules"

sudo groupadd apex

sudo adduser $USER apex


# Update the boot configuration for Raspberry Pi
echo "kernel=kernel8.img" | sudo tee -a /boot/firmware/config.txt

# Back up the Device Tree Blob (DTB) 
sudo cp /boot/firmware/bcm2712-rpi-5-b.dtb /boot/firmware/bcm2712-rpi-5-b.dtb.bak 

# Decompile the DTB into a DTS file 
sudo dtc -I dtb -O dts /boot/firmware/bcm2712-rpi-5-b.dtb -o ~/test.dts 

# Modify the Device Tree Source (DTS) 
sudo sed -i '/pcie@110000 {/,/};/{/msi-parent = <[^>]*>;/{s/msi-parent = <[^>]*>;/msi-parent = <0x67>;/}}' ~/test.dts

# Recompile the DTS back into a DTB 
sudo dtc -I dts -O dtb ~/test.dts -o ~/test.dtb 

# Replace the old DTB with the new one 
sudo mv ~/test.dtb /boot/firmware/bcm2712-rpi-5-b.dtb

sudo reboot now
