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
    libbz2-dev

# Install Python 3.9
RUN wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz

RUN tar -xzvf Python-3.9.1.tgz && cd Python-3.9.1
RUN ./configure --enable-optimizations
RUN make -j 4
RUN make altinstall

# Install dependencies
RUN apt-get update && apt-get install -y \
    libedgetpu1-std \
    gnupg \
    gnupg2 \
    gnupg1 \
    && apt-get clean

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    tee /etc/apt/sources.list.d/coral-edgetpu.list

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# Install Pycoral
RUN pip3 install pycoral

# Set the default Python version to 3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Create a directory for the Pycoral scripts
WORKDIR /pycoral

# Copy any local scripts into the container
COPY . /pycoral

# Set the entrypoint
ENTRYPOINT ["python3"]
EOF

# Build the Docker image
docker build -t pycoral:debian-bullseye .

# Run a container from the image
docker run -it --rm --privileged --device /dev/apex_0:/dev/apex_0 debian:10
