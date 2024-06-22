sudo apt update
sudo apt upgrade

# Install Edge TPU runtime
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt update
sudo apt install libedgetpu1-std

sudo python3 install --upgrade pip
sudo pip3.9 install --upgrade pip

sudo apt-get update
sudo apt-get install libcap-dev

sudo apt-get install -y build-essential cmake pkg-config python3-dev libjpeg-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libxslt1-dev libxml2-dev meson ninja-build

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip
sudo pip3 install meson
sudo apt-get install ninja-build

sudo apt-get install -y build-essential cmake pkg-config python3-dev libjpeg-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libxslt1-dev libxml2-dev

sudo pip3 install jinja2 ply pyyaml pybind11 virtualenv 

sudo apt install screen xclip

# Install Python packages
sudo apt install python3-pip
pip3 install numpy pillow tflite-runtime
pip3 install opencv-python-headless
pip3 install picamera2

