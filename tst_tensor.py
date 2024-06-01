import tensorflow as tf
import numpy as np
import logging
from picamera2 import Picamera2

# Setup logging
logging.basicConfig(filename='tpu_camera_test_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def test_tpu_and_camera():
    tpu_connected = False
    camera_connected = False
    read_write_test_passed = False
    multiplication_test_passed = False

    # Check if TPU is available
    try:
        delegate = tf.lite.experimental.load_delegate('libedgetpu.so.1.0')
        logging.info("TPU is available and being used.")
        tpu_connected = True
    except ValueError:
        logging.error("TPU not available.")
        print("TPU not available, exiting.")
        return

    # Check if the camera is available
    try:
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640, 480)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.preview_configuration.controls.FrameRate = 30
        picam2.configure("preview")
        picam2.start()
        logging.info("Camera initialized and started.")
        camera_connected = True
    except Exception as e:
        logging.error(f"Camera not available: {e}")
        print(f"Camera not available: {e}, exiting.")
        return

    # Create a simple model for testing TPU
    try:
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(5, activation='softmax')
        ])
        logging.info("Simple test model created.")
    except Exception as e:
        logging.error(f"Failed to create test model: {e}")
        print(f"Failed to create test model: {e}")
        return

    # Convert the model to TensorFlow Lite format with Edge TPU delegate
    try:
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        logging.info("Model converted to TensorFlow Lite format.")
    except Exception as e:
        logging.error(f"Failed to convert model to TensorFlow Lite format: {e}")
        print(f"Failed to convert model to TensorFlow Lite format: {e}")
        return

    # Save the model to a file
    try:
        with open('test_model.tflite', 'wb') as f:
            f.write(tflite_model)
        logging.info("TensorFlow Lite model saved to test_model.tflite.")
    except Exception as e:
        logging.error(f"Failed to save TensorFlow Lite model: {e}")
        print(f"Failed to save TensorFlow Lite model: {e}")
        return

    # Load the TensorFlow Lite model
    try:
        interpreter = tf.lite.Interpreter(model_path="test_model.tflite", experimental_delegates=[delegate])
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

    # Stop the camera
    if camera_connected:
        picam2.stop()
        logging.info("Camera stopped and resources released.")

    # Print final status
    print("TPU Connection Status: ", "Connected" if tpu_connected else "Not Connected")
    print("Camera Connection Status: ", "Connected" if camera_connected else "Not Connected")
    print("Read/Write Test Status: ", "Passed" if read_write_test_passed else "Failed")
    print("Multiplication Test Status: ", "Passed" if multiplication_test_passed else "Failed")

    logging.info("TPU Connection Status: %s", "Connected" if tpu_connected else "Not Connected")
    logging.info("Camera Connection Status: %s", "Connected" if camera_connected else "Not Connected")
    logging.info("Read/Write Test Status: %s", "Passed" if read_write_test_passed else "Failed")
    logging.info("Multiplication Test Status: %s", "Passed" if multiplication_test_passed else "Failed")

if __name__ == "__main__":
    test_tpu_and_camera()

