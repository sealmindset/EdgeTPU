# Use Debian 10 as the base image
FROM debian:10

# Set the working directory
WORKDIR /home
ENV HOME /home

# Install necessary packages
RUN apt-get update && \
    apt-get install -y git vim python3-pip python-dev pkg-config wget curl dkms rsync build-essential cmake unzip

# Install zlib and other required libraries
RUN apt-get install -y zlib1g-dev libjpeg-dev libpng-dev

# Add the Coral Edge TPU repository and install Edge TPU packages
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y libedgetpu1-std libedgetpu-dev

# Download and install specific kernel headers (example kernel version)
RUN wget https://github.com/raspberrypi/linux/archive/refs/tags/raspberrypi-kernel_1.20210527-1.tar.gz && \
    tar -xzf raspberrypi-kernel_1.20210527-1.tar.gz && \
    cd linux-raspberrypi-kernel_1.20210527-1 && \
    make headers_install INSTALL_HDR_PATH=/usr

# Install additional tools
RUN apt-get install -y udev sudo

# Set up udev rules for the Coral PCIe TPU
RUN echo 'SUBSYSTEM=="pci", ATTRS{vendor}=="0x1ac1", ATTRS{device}=="0x089a", MODE="0666"' > /etc/udev/rules.d/99-coral-pcie.rules

# Install Docker-specific dependencies (if needed)
RUN apt-get install -y docker.io

# Download and install tflite-runtime
RUN wget https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_aarch64.whl
RUN pip3 install tflite_runtime-2.5.0-cp37-cp37m-linux_aarch64.whl

# Install numpy and pillow
RUN pip3 install numpy pillow

# Remove the EXTERNALLY-MANAGED file if it exists
RUN if [ -f /usr/lib/python3.11/EXTERNALLY-MANAGED ]; then \
        rm /usr/lib/python3.11/EXTERNALLY-MANAGED; \
    fi

# Download the TensorFlow Lite model
RUN wget -O efficientdet_lite0.tflite https://github.com/schu-lab/Tensorflow-Object-Detection/raw/main/efficientdet_lite0.tflite

# Expose necessary ports (if applicable)
EXPOSE 8080

# Set entrypoint or command (if applicable)
CMD ["bash"]
