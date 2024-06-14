import logging
import time
import threading
from pathlib import Path
from PIL import Image
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import detect

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_image(image_path):
    return Image.open(image_path).convert('RGB')

def run_inference(interpreter, image):
    common.set_input(interpreter, image)
    interpreter.invoke()
    return detect.get_objects(interpreter, score_threshold=0.4)

def stress_test_tpu(model_path, image_path, iterations=100):
    try:
        logger.info(f"Running stress test on TPU with model: {model_path}")

        # Load model and allocate tensors
        interpreter = make_interpreter(str(model_path))  # Convert Path to string
        interpreter.allocate_tensors()

        # Prepare input
        size = common.input_size(interpreter)
        image = load_image(image_path).resize(size, Image.Resampling.LANCZOS)  # Updated resampling method

        for i in range(iterations):
            start = time.perf_counter()
            objs = run_inference(interpreter, image)
            inference_time = time.perf_counter() - start
            logger.info(f"Inference {i+1}/{iterations}: {inference_time * 1000:.2f} ms")

        logger.info("Stress test completed successfully.")

    except Exception as e:
        logger.error(f"Error during stress test execution: {e}", exc_info=True)
        return False

def main():
    model_path = Path("test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
    image_path = Path("test_data/grace_hopper.bmp")
    iterations = 100

    # You can run multiple threads to increase the load
    threads = []
    for i in range(4):  # Adjust the number of threads based on your TPU capabilities
        t = threading.Thread(target=stress_test_tpu, args=(model_path, image_path, iterations))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    logger.info("All stress test threads completed.")

if __name__ == "__main__":
    main()
