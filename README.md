
# Raspberry Pi Camera Capture & Streaming Utility

This repository provides a professional, privacy-safe FastAPI application and camera utility class for handling camera operations on a Raspberry Pi using the Picamera2 library. The code demonstrates best practices for initializing, configuring, capturing images, and streaming video from the camera, with thread safety and error handling. All sensitive or company-specific logic has been removed or replaced with placeholders.

## Features
- Initialize and configure the camera with custom resolutions and exposure time
- Capture high-resolution still images
- Stream video frames efficiently via a FastAPI endpoint
- Thread-safe image capture for use in multi-threaded applications
- Graceful error handling and resource management
- Simple web UI and REST API for demonstration

## Usage Example
### 1. Camera Utility (capturing_public.py)
```python
from capturing_public import capturing

# Initialize camera handler
cap = capturing()

# Capture a single image
image = cap.capture_single()

# Start video streaming (generator)
for frame in cap.start_stream():
    # Process frame (e.g., send to web client)
    pass

# Stop streaming
cap.stop_stream()
```

### 2. FastAPI Application (main_public.py)
Run the FastAPI app for a web interface and REST API:
```bash
uvicorn main_public:app --reload
```
Visit `http://localhost:8000` for the dashboard (if templates are provided), or use `/video_feed` for the video stream.

## Privacy & Security
- All sensitive credentials, server logic, and company-specific code have been removed or replaced with placeholders.
- This repository is safe for public sharing and demonstration.

## Requirements
- Python 3.8+
- picamera2
- opencv-python
- numpy
- fastapi
- uvicorn

## License
MIT License
