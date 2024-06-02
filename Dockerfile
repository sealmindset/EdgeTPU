# Use Debian 10 as the base image
FROM debian:10

# Set the working directory
WORKDIR /home
ENV HOME /home

# Install necessary packages
RUN apt-get update && \
    apt-get install -y git nano python3-pip python-dev pkg-config wget curl dkms rsync build-essential cmake unzip

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

# Install Python packages
RUN pip3 install numpy pillow

# Download TensorFlow Lite source and build it
RUN wget -O tensorflow.zip https://github.com/tensorflow/tensorflow/archive/v2.5.0.zip && \
    unzip tensorflow.zip && \
    mv tensorflow-2.5.0 tensorflow && \
    cd tensorflow && \
    ./tensorflow/lite/tools/make/download_dependencies.sh && \
    ./tensorflow/lite/tools/make/build_aarch64_lib.sh

# Copy the built TensorFlow Lite library
RUN cp /home/tensorflow/tensorflow/lite/tools/make/gen/linux_aarch64/lib/libtensorflow-lite.a /usr/local/lib/
RUN cp -r /home/tensorflow/tensorflow/lite/tools/make/gen/linux_aarch64/lib/* /usr/local/lib/

# Expose necessary ports (if applicable)
EXPOSE 8080

# Set entrypoint or command (if applicable)
CMD ["bash"]
