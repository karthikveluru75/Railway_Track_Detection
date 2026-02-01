import cv2
import os
import re

def create_video_from_images(image_folder, output_video_name, fps=1):
    """
    Creates a video from a sequence of images in a folder.
    
    Args:
        image_folder (str): Path to the folder containing images.
        output_video_name (str): Filename for the output video.
        fps (int): Frames per second.
    """
    # Get all jpg files in the folder
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    
    # Sort images naturally (r0_c0, r0_c1, etc.)
    # Standard string sort can be incorrect for numbers (e.g. 10 comming before 2)
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]
    
    images.sort(key=natural_sort_key)

    if not images:
        print("No images found in the folder.")
        return

    # Read the first image to get width and height dimensions for the video
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    # 'mp4v' is a common codec for creating .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(output_video_name, fourcc, fps, (width, height))

    print(f"Creating video: {output_video_name}...")
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        
        # Ensure all images are the same size as the first one
        # If sizes differ, the video writer might fail or produce artifacts
        if (frame.shape[1], frame.shape[0]) != (width, height):
            frame = cv2.resize(frame, (width, height))
            
        video.write(frame)

    # Release the video writer to save the file
    video.release()
    print(f"Video saved successfully as {output_video_name}")

if __name__ == "__main__":
    # Define folder paths
    # Ensure this path exists and contains your split images
    folder_path = r'C:\Users\prath\OneDrive\Desktop\heart_dieases\split_images'
    output_name = 'animal_slideshow.mp4'
    
    # Create the video
    # fps=2 means 2 image per second. Increase it for a faster video.
    create_video_from_images(folder_path, output_name, fps=2)
