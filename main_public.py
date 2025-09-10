
"""
main_public.py
----------------
A privacy-safe, professional FastAPI application for Raspberry Pi camera capture and streaming.
Sensitive commands, credentials, and company logic have been removed or replaced with placeholders.
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import logging
import cv2
from capturing_public import capturing
from PIL import Image, UnidentifiedImageError

# Initialize camera handler and FastAPI app
CAP = capturing()
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Set up static files and templates (for web UI)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Video streaming endpoint
@app.get('/video_feed')
def video_feed():
    """
    Streams video frames from the Raspberry Pi camera as multipart JPEG.
    """
    return StreamingResponse(CAP.start_stream(), media_type='multipart/x-mixed-replace; boundary=frame')

# Capture image and save locally
@app.post('/capture_img')
def capture_img():
    """
    Captures a single image and saves it to the output directory.
    """
    img = CAP.capture_single()
    if img is None:
        logging.error("Failed to capture image: Camera might not be initialized properly.")
        return {"message": "Failed to capture image: Camera might not be initialized properly."}
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"captured_image_{timestamp}.jpg"
    local_path = f"static/output/{filename}"
    try:
        cv2.imwrite(local_path, img)
        logging.info(f"Image saved locally as {local_path}")
    except cv2.error as e:
        logging.error(f"Failed to save the captured image: {e}")
        return {"message": "Failed to save the captured image."}
    return {
        "message": "Image has been captured and saved successfully.",
        "image_url": f"/static/output/{filename}"
    }

# Root route to load main page (dashboard)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Load photostorage page and display images
@app.get("/photostorage", response_class=HTMLResponse)
async def read_photostorage(request: Request):
    images = get_images()
    return templates.TemplateResponse("photostorage.html", {"request": request, "images": images})

# Utility to list captured images
def get_images():
    IMAGE_DIR = "static/output"
    images = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(IMAGE_DIR, filename)
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    timestamp_str = filename[len("captured_image_"):-len(".jpg")]
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                    images.append({
                        "url": f"/static/output/{filename}",
                        "timestamp": timestamp.isoformat(),
                        "filename": filename
                    })
            except UnidentifiedImageError:
                print(f"Cannot identify image file {image_path}, skipping.")
    return images

# API endpoint to get image metadata as JSON
@app.get("/get_images")
def get_images_route():
    return JSONResponse(content=get_images())

# API endpoint to stop the video stream
@app.post('/stop_stream')
async def stop_stream():
    CAP.stop_stream()
    return JSONResponse(content={"message": "Streaming stopped successfully."})

# API endpoint to get battery status (mocked for privacy)
@app.get("/battery_status")
async def battery_status():
    # Replace with actual battery reading logic if desired
    return {"capacity": 100.0}  # Example static value

# Start the server (for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
