#!/bin/bash

# Add the Google Coral Edge TPU repository to the system's source list
# This repository contains packages specifically for the Coral Edge TPU
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

# Download and add the Google GPG key to the system
# This key is used to ensure the integrity and authenticity of the packages
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package lists for packages that need upgrading, as well as new packages that have just come to the repositories
sudo apt update
sudo apt upgrade

# Install the kernel module for Google's Gasket driver framework
# Option 1: from repository - still doesn't work for kernel 6.6.20
# Option 2: from source

# Option 1 - BEGIN
  # sudo apt-get install gasket-dkms -y
# Option 1 - END

# Option 2 - BEGIN
  # Install packages required for building gasket-driver
  sudo apt install curl devscripts debhelper dh-dkms -y

  # Clone gasket-driver from GitHub repository
  git clone https://github.com/google/gasket-driver.git

  # Build gasket-driver deb package
  cd gasket-driver; debuild -us -uc -tc -b; cd ..

  # Install gasket-driver from deb package
  sudo dpkg -i gasket-dkms_1.0-18_all.deb
# Option 2 - END

# load the gasket-driver
sudo depmod -a
sudo modprobe apex

# Install the Edge TPU runtime
sudo apt-get install libedgetpu1-std -y

# Add 'kernel=kernel8.img' to the boot configuration
# This sets the kernel image to be used by the Raspberry Pi
echo "kernel=kernel8.img" | sudo tee -a /boot/firmware/config.txt

# Back up the current Device Tree Blob (DTB) file for Raspberry Pi
# A DTB is a binary file that contains hardware information used by the operating system
sudo cp /boot/firmware/bcm2712-rpi-5-b.dtb /boot/firmware/bcm2712-rpi-5-b.dtb.bak

# Decompile the DTB into a Device Tree Source (DTS) file for editing
# - Ignore any warnings during decompilation
sudo dtc -I dtb -O dts /boot/firmware/bcm2712-rpi-5-b.dtb -o ~/test.dts

# Modify the Device Tree Source
# Replace 'msi-parent' value to change the Message Signaled Interrupts (MSI) parent setting
sudo sed -i '/pcie@110000 {/,/msi-parent = <0x2[fc]>;/{s/<0x2f>/<0x67>/; s/<0x2c>/<0x67>/}' ~/test.dts

# Recompile the DTS back into a DTB
sudo dtc -I dts -O dtb ~/test.dts -o ~/test.dtb

# Replace the old DTB with the new one
sudo mv ~/test.dtb /boot/firmware/bcm2712-rpi-5-b.dtb

# Reboot the system to apply changes
sudo reboot now
