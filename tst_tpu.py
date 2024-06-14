import os
import subprocess
import sys
from pathlib import Path
from PIL import Image
from colorama import init, Fore, Style
import logging
import traceback

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def print_task(message):
    print(Fore.YELLOW + message)

def print_result(message):
    print(Fore.GREEN + message)

def print_error(message):
    print(Fore.RED + message)

def print_output(message):
    print(Fore.WHITE + message)

def install_package(package):
    print_task(f"Installing package: {package}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--extra-index-url", "https://google-coral.github.io/py-repo/", package])
        print_result(f"{package} installed successfully.")
    except subprocess.CalledProcessError as e:
        print_error(f"Error installing {package}: {e}")
        sys.exit(1)

def check_and_install_packages(packages):
    for package in packages:
        try:
            __import__(package)
            print_result(f"{package} is already installed.")
        except ImportError:
            print_task(f"{package} not found, installing...")
            install_package(package)

def run_command(command):
    print_task(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        print_output(f"Command output: {output}")
        return output
    except subprocess.CalledProcessError as e:
        print_error(f"Command '{command}' failed with error: {e.stderr.decode('utf-8').strip()}")
        sys.exit(1)

def check_tpu_presence():
    print_task("Checking for TPU presence...")
    lspci_output = run_command("lspci")
    if "Coral Edge TPU" in lspci_output:
        print_result("TPU detected successfully.")
    else:
        print_error("TPU not detected in lspci output.")
        sys.exit(1)

def check_permissions():
    print_task("Checking user permissions...")
    user = os.getlogin()
    groups = run_command(f"groups {user}")
    if "plugdev" in groups and "apex" in groups:
        print_result("User has correct permissions.")
    else:
        if "plugdev" not in groups:
            print_task("User not in 'plugdev' group. Adding user to 'plugdev' group...")
            run_command(f"sudo usermod -aG plugdev {user}")
        if "apex" not in groups:
            print_task("User not in 'apex' group. Adding user to 'apex' group...")
            run_command(f"sudo usermod -aG apex {user}")
        print_result("Please log out and log back in for the changes to take effect.")
        sys.exit(1)

def clone_repo(repo_url, repo_dir):
    if not repo_dir.exists():
        print_task(f"Cloning repository from {repo_url}...")
        run_command(f"git clone {repo_url} {repo_dir}")
        print_result("Repository cloned successfully.")
    else:
        print_result(f"Repository {repo_dir} already exists, skipping clone.")

def clone_test_data():
    repo_url = "https://github.com/google-coral/test_data.git"
    repo_dir = Path("test_data")
    clone_repo(repo_url, repo_dir)

def clone_pycoral():
    repo_url = "https://github.com/google-coral/pycoral.git"
    repo_dir = Path("pycoral")
    clone_repo(repo_url, repo_dir)

def run_pycoral_classification_example():
    print_task("Running PyCoral classification example...")
    try:
        example_script = Path("pycoral/examples/classify_image.py")
        model_path = Path("test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite")
        labels_path = Path("test_data/inat_bird_labels.txt")
        image_path = Path("test_data/parrot.jpg")

        command = f"python3 {example_script} --model {model_path} --labels {labels_path} --input {image_path}"
        run_command(command)
    except Exception as e:
        print_error(f"Error running PyCoral classification example: {e}")
        traceback.print_exc()
        sys.exit(1)

def run_pycoral_detection_example():
    print_task("Running PyCoral detection example...")
    try:
        example_script = Path("pycoral/examples/detect_image.py")
        model_path = Path("test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
        labels_path = Path("test_data/coco_labels.txt")
        input_image_path = Path("test_data/grace_hopper.bmp")
        output_image_path = Path("grace_hopper_processed.bmp")

        command = f"python3 {example_script} --model {model_path} --labels {labels_path} --input {input_image_path} --output {output_image_path}"
        run_command(command)
    except Exception as e:
        print_error(f"Error running PyCoral detection example: {e}")
        traceback.print_exc()
        sys.exit(1)

def stress_test_tpu(model_path, image_path, iterations=100):
    try:
        logger.info(f"Running stress test on TPU with model: {model_path}")

        from pycoral.utils.edgetpu import make_interpreter
        from pycoral.adapters import common
        from pycoral.adapters import detect

        interpreter = make_interpreter(str(model_path))  # Convert Path to string
        interpreter.allocate_tensors()

        # Prepare input
        size = common.input_size(interpreter)
        image = Image.open(image_path).convert('RGB').resize(size, Image.Resampling.LANCZOS)

        for i in range(iterations):
            start = time.perf_counter()
            common.set_input(interpreter, image)
            interpreter.invoke()
            objs = detect.get_objects(interpreter, score_threshold=0.4)
            inference_time = time.perf_counter() - start
            logger.info(f"Inference {i+1}/{iterations}: {inference_time * 1000:.2f} ms")

        logger.info("Stress test completed successfully.")

    except Exception as e:
        logger.error(f"Error during stress test execution: {e}", exc_info=True)
        return False

def main():
    try:
        # Upgrade pycoral
        print_task("Upgrading pycoral...")
        install_package("pycoral")

        print_task("Checking and installing necessary packages...")
        packages = ["numpy", "pycoral", "colorama"]
        check_and_install_packages(packages)
        
        print_task("Checking for TPU presence...")
        check_tpu_presence()
        
        print_task("Checking user permissions...")
        check_permissions()
        
        print_task("Checking and cloning test data repository...")
        clone_test_data()

        print_task("Cloning PyCoral repository...")
        clone_pycoral()

        print_task("Running PyCoral classification example...")
        run_pycoral_classification_example()
        
        print_task("Running PyCoral detection example...")
        run_pycoral_detection_example()

        print_task("Running TPU stress test...")
        model_path = Path("test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
        image_path = Path("test_data/grace_hopper.bmp")
        stress_test_tpu(model_path, image_path)
        
        print_result("All tests completed successfully.")
    
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
