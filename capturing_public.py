import cv2
import numpy as np
import time
from picamera2 import Picamera2
from threading import Thread, Lock


# Professional, privacy-safe camera capture and streaming class for Raspberry Pi using Picamera2.
# This class demonstrates best practices for camera management, thread safety, and error handling.
class capturing:
    def __init__(self, capture_resolution=(2592, 1944), streaming_resolution=(640, 480), exposure_time=20000):
        """
        Initialize the capturing class with default resolutions and exposure time.
        Args:
            capture_resolution (tuple): Resolution for still image capture.
            streaming_resolution (tuple): Resolution for video streaming.
            exposure_time (int): Camera exposure time in microseconds.
        """
        self.capture_resolution = capture_resolution
        self.streaming_resolution = streaming_resolution
        self.exposure_time = exposure_time
        self.cam_control = {"ExposureTime": self.exposure_time}
        self.streaming = False
        self.picam2 = None
        self.lock = Lock()
        self.initialize_camera()

    def initialize_camera(self):
        """
        Initialize the camera and set the initial controls.
        Handles camera startup and applies exposure settings.
        """
        try:
            self.picam2 = Picamera2()
            self.picam2.start()
            time.sleep(2)  # Allow the camera to warm up
            self.picam2.set_controls(self.cam_control)
        except RuntimeError as e:
            print(f"Failed to initialize camera: {e}")
            self.picam2 = None

    def configure_camera(self, resolution, format="RGB888"):
        """
        Configure the camera with the given resolution and format.
        Args:
            resolution (tuple): Desired resolution.
            format (str): Pixel format (default: 'RGB888').
        """
        if self.picam2:
            self.picam2.stop()  # Stop camera before reconfiguring
            config = self.picam2.create_still_configuration(main={"size": resolution, "format": format})
            self.picam2.configure(config)
            self.picam2.set_controls(self.cam_control)
            self.picam2.start()  # Restart camera after configuring

    def capture_single(self):
        """
        Capture a single image with the configured resolution.
        Returns:
            np.ndarray or None: Captured image array, or None if camera is not initialized.
        """
        if self.picam2:
            with self.lock:
                self.configure_camera(self.capture_resolution)
                image = self.picam2.capture_array()
                self.configure_camera(self.streaming_resolution)  # Restore streaming config
            return image
        else:
            print("Camera is not initialized.")
            return None

    def start_stream(self):
        """
        Generator for streaming video frames from the camera as JPEG byte arrays.
        Yields:
            bytes: JPEG-encoded video frame for HTTP streaming.
        """
        if self.picam2:
            self.configure_camera(self.streaming_resolution)
            self.streaming = True
            while self.streaming:
                try:
                    with self.lock:
                        frame = self.picam2.capture_buffer(name="main")
                    frame = np.frombuffer(frame, np.uint8).reshape(self.streaming_resolution[1], self.streaming_resolution[0], 3)
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    self.stop_stream()
                time.sleep(0.05)  # Throttle streaming to avoid resource exhaustion

    def stop_stream(self):
        """
        Stop the video stream and release camera resources.
        """
        self.streaming = False
        if self.picam2:
            self.picam2.stop()

    def capture_image_thread(self):
        """
        Capture an image in a separate thread (non-blocking).
        Useful for background image capture during streaming.
        """
        thread = Thread(target=self.capture_single)
        thread.start()
