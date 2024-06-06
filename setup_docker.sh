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
FROM debian:bullseye

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    libedgetpu1-std \
    && apt-get clean

# Remove the EXTERNALLY-MANAGED file if it exists
RUN if [ -f /usr/lib/python3.11/EXTERNALLY-MANAGED ]; then \
        rm /usr/lib/python3.11/EXTERNALLY-MANAGED; \
    fi

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
