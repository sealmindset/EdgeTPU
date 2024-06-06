#!/bin/bash

# Update and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to the docker group
sudo usermod -aG docker $USER
newgrp docker

# Create a Dockerfile for Pycoral
cat <<EOF > Dockerfile
FROM debian:10

# Python dependencies
RUN sudo apt install build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    curl \
    wget \
    pciutils \
    libbz2-dev

# Install Python 3.9
RUN wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz

RUN tar -xzvf Python-3.9.1.tgz && cd Python-3.9.1
RUN ./configure --enable-optimizations
RUN make -j 4
RUN make altinstall

RUN ln -s /usr/local/bin/python3.9 /usr/local/bin/python3
RUN ln -s /usr/local/bin/python3.9 /usr/local/bin/python

RUN apt-get update && apt-get install python3-pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN apt-get update && apt-get install -y \
    libedgetpu1-std \
    gnupg \
    gnupg2 \
    gnupg1 \
    && apt-get clean

RUN apt-get install build-essential \
    cmake \
    git \
    unzip \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgtk2.0-dev \
    libcanberra-gtk* \
    libgtk-3-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-gtk3 \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-gl \
    libxvidcore-dev \
    libx264-dev \
    python3-dev \
    python3-numpy \
    libtbb2 \
    libtbb-dev \
    libdc1394-22-dev \
    libv4l-dev \
    v4l-utils \
    libopenblas-dev \
    libatlas-base-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libhdf5-dev \
    libprotobuf-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    protobuf-compiler \
    && apt-get clean

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    tee /etc/apt/sources.list.d/coral-edgetpu.list

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# Install Pycoral
RUN apt-get update
RUN pip3 install pycoral

RUN apt-get update
RUN apt-get install python3-tflite-runtime

# Coral
RUN mkdir google-coral && cd google-coral
RUN git clone https://github.com/google-coral/examples-camera --depth 1

RUN pip3 install opencv-contrib-python
RUN apt-get install python3-opencv

# Tensorflow
RUN pip3 install tensorflow

# Create a directory for the Pycoral scripts
WORKDIR /pycoral

# Copy any local scripts into the container
COPY . /pycoral

# Set the entrypoint
ENTRYPOINT ["python3"]
EOF
