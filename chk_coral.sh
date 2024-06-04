#!/bin/bash

# Check if the Gasket driver is loaded
if lsmod | grep -q "gasket"; then
    echo "Gasket driver is loaded."
else
    echo "Gasket driver is not loaded. Please check the installation."
    exit 1
fi

# Check if the Apex device is available
if [ -e /dev/apex_0 ]; then
    echo "Apex device is available."
else
    echo "Apex device is not available. Please check the Gasket driver and udev rules."
    exit 1
fi

# Check if the user is in the apex group
if id -nG "$USER" | grep -qw "apex"; then
    echo "User is in the apex group."
else
    echo "User is not in the apex group. Please add the user to the apex group."
    exit 1
fi

echo "All checks passed. Coral Edge TPU is set up correctly."
