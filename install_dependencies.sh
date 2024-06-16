#!/bin/bash

set -e

# Function to install or upgrade a package
install_or_upgrade() {
    package=$1
    if dpkg -l | grep -q "^ii.*$package"; then
        echo "Upgrading $package..."
        sudo apt-get install --only-upgrade -y $package
    else
        echo "Installing $package..."
        sudo apt-get install -y $package
    fi
}

# Function to install Python package
pip_install_or_upgrade() {
    package=$1
    if pip3 show $package &>/dev/null; then
        echo "Upgrading $package..."
        pip3 install --upgrade $package
    else
        echo "Installing $package..."
        pip3 install $package
    fi
}

# List of required packages
required_packages=(
    "python3-picamera2"
    "libatlas-base-dev"
    "gfortran"
    "libjpeg-dev"
    "libopenjp2-7"
    "libtiff5-dev"
    "python3-pyqt5"
    "libqt5gui5"
    "libqt5test5"
    "libimath-dev"
    "libopenexr-dev"
    "libgstreamer1.0-0"
    "gstreamer1.0-tools"
    "gstreamer1.0-plugins-base"
    "gstreamer1.0-plugins-good"
    "gstreamer1.0-plugins-bad"
    "gstreamer1.0-plugins-ugly"
    "gstreamer1.0-alsa"
    "gstreamer1.0-pulseaudio"
    "libcap-dev"  # Added to handle python-prctl dependency
    "libgdal-dev" # Added to handle fiona dependency
)

# List of required Python packages
required_python_packages=(
    "picamera2"
    "pycoral"
    "python-prctl"  # Added python-prctl explicitly
    "fiona"         # Added fiona explicitly
)

# Update package list
sudo apt-get update

# Install or upgrade required packages
for package in "${required_packages[@]}"; do
    while true; do
        if install_or_upgrade $package; then
            break
        else
            echo "Error installing $package. Checking for specific handling..."
            if [[ "$package" == "libtiff5" ]]; then
                echo "Attempting to install libtiff5-dev instead..."
                if sudo apt-get install -y libtiff5-dev; then
                    echo "libtiff5-dev installed successfully."
                    break
                else
                    echo "Failed to install libtiff5-dev. Retrying..."
                fi
            elif [[ "$package" == "libilmbase25" ]]; then
                echo "Attempting to install lib{imath,openexr,ilmbase}-dev instead..."
                if sudo apt-get install -y --mark-auto libimath-dev libopenexr-dev; then
                    echo "libimath-dev and libopenexr-dev installed successfully."
                    break
                else
                    echo "Failed to install libimath-dev and libopenexr-dev. Retrying..."
                fi
            elif [[ "$package" == "libgdal-dev" ]]; then
                echo "Attempting to install libgdal-dev for GDAL support..."
                if sudo apt-get install -y libgdal-dev; then
                    echo "libgdal-dev installed successfully."
                    break
                else
                    echo "Failed to install libgdal-dev. Retrying..."
                fi
            else
                echo "Retrying to install $package..."
            fi
            sleep 2
        fi
    done
done

# Install or upgrade required Python packages
for package in "${required_python_packages[@]}"; do
    until pip_install_or_upgrade $package; do
        echo "Retrying to install $package..."
        sleep 2
    done
done

echo "All packages are installed and up-to-date."
