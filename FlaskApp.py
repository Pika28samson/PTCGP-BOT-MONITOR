from flask import Flask, send_file, render_template
import os
import time
import threading
import pyautogui

app = Flask(__name__)
UPLOAD_FOLDER = r"c:\\Me\\Python Projects\\MirrorScreen\\uploads\\"
IMAGE_NAME = "latest_image.jpg"

tabs=3
box = (0, 0, 278*tabs, 540)

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to serve the latest image
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    image_path = UPLOAD_FOLDER +IMAGE_NAME
    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        return "No image uploaded yet.", 404

def upload_image():
    while True:
        curTime = time.time()
        try:
            # Take a screenshot using pyautogui
            screenshot = pyautogui.screenshot()
            screenshot = screenshot.crop(box)
            
            # Path to save the image
            dest_path = os.path.join(UPLOAD_FOLDER, IMAGE_NAME)
            
            # Check if the directory exists and print the path
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            screenshot.save(dest_path, "JPEG")
            print(f"Image saved at {dest_path}")

        except Exception as e:
            print(f"Error while saving screenshot: {e}")

        # Wait for 10 seconds before capturing the next screenshot
        while time.time()-curTime<1:
            pass


# Start the background thread
threading.Thread(target=upload_image, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
