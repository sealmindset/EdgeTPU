import argparse
import sys
import time

import cv2
import mediapipe as mp

from picamera2 import Picamera2, Preview
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils import visualize

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()

def save_image(image, filename="output.jpg"):
    cv2.imwrite(filename, image)

def run(model: str, max_results: int, score_threshold: float, 
        width: int, height: int, record_duration: int) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
      model: Name of the TFLite object detection model.
      max_results: Max number of detection results.
      score_threshold: The score threshold of detection results.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
      record_duration: Number of seconds to record the video.
    """

    # Start capturing video input from the CSI camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (width, height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 30
    picam2.configure("preview")
    picam2.start()

    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    detection_frame = None
    detection_result_list = []

    def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME

        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        detection_result_list.append(result)
        COUNTER += 1

    # Initialize the object detection model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           running_mode=vision.RunningMode.LIVE_STREAM,
                                           max_results=max_results, score_threshold=score_threshold,
                                           result_callback=save_result)
    detector = vision.ObjectDetector.create_from_options(options)

    # Start time for recording duration
    recording_start_time = time.time()

    # Continuously capture images from the camera and run inference
    while True:
        current_time = time.time()
        if current_time - recording_start_time >= record_duration:
            break

        image = picam2.capture_array()
        if image is None:
            sys.exit(
                'ERROR: Unable to read from CSI camera. Please verify your camera settings.'
            )

        image = cv2.flip(image, 1)

        # Convert the image from RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run object detection using the model.
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(FPS)
        text_location = (left_margin, row_size)
        current_frame = image
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                    font_size, text_color, font_thickness, cv2.LINE_AA)

        if detection_result_list:
            current_frame = visualize(current_frame, detection_result_list[0])
            detection_frame = current_frame
            detection_result_list.clear()

        if detection_frame is not None:
            save_image(detection_frame, "detection_output.jpg")

    detector.close()
    picam2.stop()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--maxResults',
        help='Max number of detection results.',
        required=False,
        default=5)
    parser.add_argument(
        '--scoreThreshold',
        help='The score threshold of detection results.',
        required=False,
        type=float,
        default=0.25)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--recordDuration',
        help='Duration of video recording in seconds.',
        required=False,
        type=int,
        default=10)
    args = parser.parse_args()

    run(args.model, int(args.maxResults),
        args.scoreThreshold, args.frameWidth, args.frameHeight, args.recordDuration)

if __name__ == '__main__':
    main()
