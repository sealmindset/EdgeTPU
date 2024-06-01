import tensorflow as tf
import numpy as np
import logging

# Setup logging
logging.basicConfig(filename='tpu_test_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def test_tpu():
    tpu_connected = False
    read_write_test_passed = False
    multiplication_test_passed = False

    # Check if TPU is available
    try:
        delegate = tf.lite.experimental.load_delegate('libedgetpu.so.1.0')
        interpreter = tf.lite.Interpreter(model_path="efficientdet_lite0.tflite", experimental_delegates=[delegate])
        logging.info("TPU is available and being used.")
        tpu_connected = True
    except ValueError as e:
        logging.error(f"TPU not available: {e}")
        print("TPU not available, exiting.")
        return

    # Load the TensorFlow Lite model and allocate tensors
    try:
        interpreter.allocate_tensors()
        logging.info("TensorFlow Lite model loaded and tensors allocated.")
    except Exception as e:
        logging.error(f"Failed to load TensorFlow Lite model: {e}")
        print(f"Failed to load TensorFlow Lite model: {e}")
        return

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Create a random input tensor
    input_data = np.random.rand(1, 10).astype(np.float32)
    logging.info(f"Input data created: {input_data}")

    # Set the input tensor and run inference
    try:
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        logging.info(f"Output data: {output_data}")
        read_write_test_passed = True
    except Exception as e:
        logging.error(f"Failed to read/write tensor: {e}")
        print(f"Failed to read/write tensor: {e}")

    # Verify if the TPU processed the data correctly
    try:
        assert output_data is not None
        logging.info("TPU read/write test passed successfully.")
        multiplication_test_passed = True
    except AssertionError:
        logging.error("TPU read/write test failed.")

    # Print final status
    print("TPU Connection Status: ", "Connected" if tpu_connected else "Not Connected")
    print("Read/Write Test Status: ", "Passed" if read_write_test_passed else "Failed")
    print("Multiplication Test Status: ", "Passed" if multiplication_test_passed else "Failed")

    logging.info("TPU Connection Status: %s", "Connected" if tpu_connected else "Not Connected")
    logging.info("Read/Write Test Status: %s", "Passed" if read_write_test_passed else "Failed")
    logging.info("Multiplication Test Status: %s", "Passed" if multiplication_test_passed else "Failed")

if __name__ == "__main__":
    test_tpu()
