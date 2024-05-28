import os
import subprocess

def check_library(library_path):
    if os.path.exists(library_path):
        print(f"Library {library_path} is installed.")
        return True
    else:
        print(f"Library {library_path} is not found.")
        return False

def load_kernel_module(module_name):
    try:
        result = subprocess.run(['sudo', 'modprobe', module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"Kernel module {module_name} loaded successfully.")
            return True
        else:
            print(f"Failed to load kernel module {module_name}.")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error loading kernel module {module_name}: {e}")
        return False

def check_kernel_module(module_name):
    try:
        result = subprocess.run(['lsmod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if module_name in result.stdout:
            print(f"Kernel module {module_name} is loaded.")
            return True
        else:
            print(f"Kernel module {module_name} is not loaded.")
            return False
    except Exception as e:
        print(f"Error checking kernel module {module_name}: {e}")
        return False

def check_tpu_device(device_path):
    if os.path.exists(device_path):
        print(f"TPU device {device_path} is present.")
        return True
    else:
        print(f"TPU device {device_path} is not found.")
        return False

def try_load_delegate(library_path):
    from tflite_runtime.interpreter import load_delegate
    try:
        delegate = load_delegate(library_path)
        print(f"Edge TPU delegate loaded successfully from {library_path}.")
        return True
    except ValueError as e:
        print(f"Failed to load Edge TPU delegate from {library_path}.")
        print(e)
        return False

def main():
    # Paths to check
    libedgetpu_path = '/usr/lib/aarch64-linux-gnu/libedgetpu.so.1'
    tpu_device_path = '/dev/apex_0'
    gasket_module_name = 'gasket'
    apex_module_name = 'apex'

    # Check the presence of the Edge TPU library
    libedgetpu_installed = check_library(libedgetpu_path)

    # Attempt to load the kernel modules
    gasket_loaded = load_kernel_module(gasket_module_name)
    apex_loaded = load_kernel_module(apex_module_name)

    # Check if the modules are loaded
    gasket_loaded = gasket_loaded and check_kernel_module(gasket_module_name)
    apex_loaded = apex_loaded and check_kernel_module(apex_module_name)

    # Check the presence of the TPU device
    tpu_device_present = check_tpu_device(tpu_device_path)

    # Try to load the TPU delegate if the library is installed
    if libedgetpu_installed:
        delegate_loaded = try_load_delegate(libedgetpu_path)
    else:
        delegate_loaded = False

    # Summarize the results
    print("\nSummary:")
    print(f"libedgetpu1-std installed: {'Yes' if libedgetpu_installed else 'No'}")
    print(f"gasket module loaded: {'Yes' if gasket_loaded else 'No'}")
    print(f"apex module loaded: {'Yes' if apex_loaded else 'No'}")
    print(f"TPU device present: {'Yes' if tpu_device_present else 'No'}")
    print(f"TPU delegate loaded: {'Yes' if delegate_loaded else 'No'}")

if __name__ == "__main__":
    main()
