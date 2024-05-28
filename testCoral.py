import os
import time
import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate

# Set the library path if necessary
os.environ['LD_LIBRARY_PATH'] = '/usr/lib/aarch64-linux-gnu/'

# Load the model and labels
MODEL_PATH = 'mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite'
LABELS_PATH = 'inat_bird_labels.txt'

# Load labels
with open(LABELS_PATH, 'r') as f:
    labels = f.read().splitlines()

# Load the TFLite model and allocate tensors.
interpreter = Interpreter(model_path=MODEL_PATH, experimental_delegates=[load_delegate('libedgetpu.so.1')])
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Check the input shape
input_shape = input_details[0]['shape']
print(f"Input shape: {input_shape}")

# Load a sample image and preprocess it
def preprocess_image(image_path, input_shape):
    image = Image.open(image_path).convert('RGB').resize((input_shape[1], input_shape[2]))
    input_data = np.expand_dims(image, axis=0)
    return input_data

# Replace 'sample_image.jpg' with the path to your test image
image_path = 'sample_image.jpg'  # Provide your sample image path here
input_data = preprocess_image(image_path, input_shape)

# Perform inference
interpreter.set_tensor(input_details[0]['index'], input_data)

start_time = time.time()
interpreter.invoke()
end_time = time.time()

# Get the results
output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)

# Find the top prediction
top_k = results.argsort()[-5:][::-1]
for i in top_k:
    print(f"{labels[i]}: {results[i]:.5f}")

print(f"Inference time: {end_time - start_time:.5f} seconds")

# Main test function
def main():
    print("Testing Coral...")
    input_data = preprocess_image(image_path, input_shape)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)
    top_k = results.argsort()[-5:][::-1]
    for i in top_k:
        print(f"{labels[i]}: {results[i]:.5f}")
    print(f"Inference time: {end_time - start_time:.5f} seconds")

if __name__ == "__main__":
    main()
