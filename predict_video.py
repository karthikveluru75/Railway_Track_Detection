from ultralytics import YOLO
import cv2
import os

def predict_on_video(model_path, video_path, output_path):
    """
    Runs YOLO object detection on a video file.
    Displays the video in real-time and saves the results.
    """
    # 1. Load the trained YOLO model
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # 2. Run prediction on the video with streaming
    print(f"Running prediction on: {video_path}")
    print("Controls: Press 'q' or ESC to quit, 'p' to pause/resume")
    
    paused = False
    
    # Use stream=True for memory efficiency and real-time display
    # This creates a generator that yields results frame by frame
    results = model.predict(
        source=video_path,
        stream=True,      # Stream results for real-time processing
        save=True,        # Also save the output video with boxes
        save_txt=True,    # Save labels to .txt
        project='inference_runs', 
        name='animal_detection'
    )
    
    # Process and display each frame
    for r in results:
        if not paused:
            # Get the annotated frame with bounding boxes
            # plot() draws the boxes on the image
            annotated_frame = r.plot()
            
            # Display the frame in a window
            cv2.imshow('Animal Detection - YOLO Predictions', annotated_frame)
        
        # Wait for key press (1ms delay) to allow window updates
        key = cv2.waitKey(1) & 0xFF
        
        # Handle keyboard controls
        if key == ord('q') or key == 27:  # 'q' or ESC to quit
            print("\nStopping video playback...")
            break
        elif key == ord('p'):  # 'p' to pause/resume
            paused = not paused
            if paused:
                print("Video paused. Press 'p' to resume.")
            else:
                print("Video resumed.")
    
    # Clean up windows
    cv2.destroyAllWindows()
    print(f"\nSuccess! Predictions are also saved in 'inference_runs/animal_detection/'")

if __name__ == "__main__":
    # Update these paths if your file names are different
    # Use relative paths so it works on any computer
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'best (1).pt')
    VIDEO_PATH = os.path.join(BASE_DIR, 'animal_slideshow.mp4')
    OUTPUT_FOLDER = 'inference_results'

    # Check if files exist before running to avoid runtime errors
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
    elif not os.path.exists(VIDEO_PATH):
        print(f"Error: Video not found at {VIDEO_PATH}")
    else:
        predict_on_video(MODEL_PATH, VIDEO_PATH, OUTPUT_FOLDER)
