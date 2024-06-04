#!/bin/bash

# Update and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y curl gnupg build-essential devscripts dkms dh-dkms

# Add Coral Edge TPU repository
if ! grep -q "coral-edgetpu-stable" /etc/apt/sources.list.d/coral-edgetpu.list; then
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
fi

# Update package list and install the Edge TPU runtime
sudo apt update
sudo apt install -y libedgetpu1-std

# Install Python 3 and pip
sudo apt install -y python3 python3-pip

# Remove the EXTERNALLY-MANAGED file
if [ -f /usr/lib/python3.11/EXTERNALLY-MANAGED ]; then
    sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
fi

# Install Pycoral
pip3 install pycoral

# Install any other dependencies required
sudo apt install -y libatlas-base-dev

# Install GDAL (gdal-config)
sudo apt-get install -y gdal-bin libgdal-dev

# Step 4: Install the Gasket Driver

# Remove the existing gasket-driver directory if it exists
if [ -d "gasket-driver" ]; then
    rm -rf gasket-driver
fi

# Clone the Gasket driver repository
git clone https://github.com/google/gasket-driver.git

# Change into the directory and build the driver
cd gasket-driver
sudo debuild -us -uc -tc -b

# Go back to the parent directory and install the built package
cd ..
sudo dpkg -i gasket-dkms_1.0-18_all.deb

# Step 5: Set Up the udev Rule

# Add a udev rule to manage device permissions
if ! grep -q "SUBSYSTEM==\"apex\"" /etc/udev/rules.d/65-apex.rules; then
    sudo sh -c "echo 'SUBSYSTEM==\"apex\", MODE=\"0660\", GROUP=\"apex\"' >> /etc/udev/rules.d/65-apex.rules"
else
    echo "udev rule for apex already exists"
fi

# Create a new group and add your user to it
if ! getent group apex > /dev/null; then
    sudo groupadd apex
else
    echo "Group apex already exists"
fi

if ! id -nG "$USER" | grep -qw "apex"; then
    sudo adduser $USER apex
else
    echo "User $USER is already in the apex group"
fi

# Check if dtoverlay=coral-pci is already in /boot/config.txt
if ! grep -q "dtoverlay=coral-pci" /boot/firmware/config.txt; then
    echo "dtoverlay=coral-pci" | sudo tee -a /boot/config.txt
else
    echo "dtoverlay=coral-pci already exists in /boot/firmware/config.txt"
fi

# Reboot the system
sudo reboot
