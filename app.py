from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2  # OpenCV dictionary for image processing
import time
import os

# Initialize Flask application
app = Flask(__name__)

# --- CONFIGURATION ---
# Use relative paths for portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'best (1).pt')
VIDEO_PATH = os.path.join(BASE_DIR, 'animal_slideshow.mp4')

# Alert Configuration settings
ALERT_PHONE_NUMBER = "999 999 9997"
ALERT_MESSAGE = "GO MESSAGE: THERE IS ANIMAL CROSS THE TRACT REDUCE THE SPEED"
COOLDOWN_SECONDS = 30  # Prevent spamming alerts (wait 30s between alerts)

# --- GLOBAL STATE ---
# Variable to track the last time an alert was sent
last_alert_time = 0

# --- LOAD MODEL ---
print(f"Loading YOLO model from {MODEL_PATH}...")
if os.path.exists(MODEL_PATH):
    try:
        # Load the YOLO model using the Ultralytics library
        model = YOLO(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
else:
    print(f"ERROR: Model file not found at {MODEL_PATH}")
    model = None

def send_alert_sms():
    """
    Simulates sending an SMS alert when an animal is detected.
    
    This function checks if the cooldown period has passed since the last alert.
    If so, it prints the alert message to the console (simulating an SMS)
    and updates the last_alert_time.
    
    Returns:
        bool: True if alert was sent, False otherwise.
    """
    global last_alert_time
    current_time = time.time()
    
    # Check if enough time has passed since the last alert (Cooldown mechanism)
    if current_time - last_alert_time > COOLDOWN_SECONDS:
        print("\n" + "!" * 60)
        print(f" ALERT TRIGGERED")
        print(f" Sending SMS to: {ALERT_PHONE_NUMBER}")
        print(f" Content: {ALERT_MESSAGE}")
        print("!" * 60 + "\n")
        
        last_alert_time = current_time
        return True
    return False

def generate_frames():
    """
    Generator function that reads the video frame-by-frame, performs object detection,
    and yields the processed frames for streaming to the web browser.
    """
    # Open the video file for reading
    cap = cv2.VideoCapture(VIDEO_PATH)
    
    if not cap.isOpened():
        print(f"Error opening video file: {VIDEO_PATH}")
        return

    while True:
        # Read a frame from the video
        success, frame = cap.read()
        if not success:
            # If video reaches the end, loop back to the start
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        if model:
            # Run YOLO inference on the frame
            # verbose=False suppresses standard output log for each prediction
            results = model.predict(frame, verbose=False)
            result = results[0]  # Get the first result
            
            # Check if any objects (boxes) are detected
            if len(result.boxes) > 0:
                # Trigger the alert simulation
                send_alert_sms()

            # Draw the bounding boxes on the frame
            # labels=False hides the class names, showing only the box
            annotated_frame = result.plot(labels=False)
        else:
            # If model failed to load, just show the raw frame without detection
            annotated_frame = frame
        
        # Encode the frame into JPEG format for network transmission
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()

        # Yield the frame in a format suitable for MJPEG streaming
        # The 'yield' keyword turns this function into a generator
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """
    Route for the home page.
    Renders the 'index.html' template which contains the video player.
    """
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """
    Route that provides the video stream.
    The <img> tag in HTML points to this URL to receive the MJPEG stream.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Start the Flask application
    # host='0.0.0.0' makes the server accessible from other devices on the same network
    # port=5000 is the standard Flask port
    print(f"Starting server... Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
