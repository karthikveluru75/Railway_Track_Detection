import cv2
import os

# ===== CONFIGURATION =====
# Define input and output directories
INPUT_DIR = "grid_images"
OUTPUT_DIR = "split_images"

# Grid configuration: 32 Images total = 8 Rows x 4 Columns
ROWS = 8
COLS = 4 

# Margin adjustments to remove grid borders
# Adjust these values if black lines persist in the output images
TOP_MARGIN = 15
BOTTOM_MARGIN = 15
LEFT_MARGIN = 15
RIGHT_MARGIN = 15
# ==================

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Iterate through all images in the input directory
for img_name in os.listdir(INPUT_DIR):
    if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
        continue # Skip non-image files

    img_path = os.path.join(INPUT_DIR, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Could not read {img_name}")
        continue

    h, w, _ = img.shape
    
    count = 0
    base_name = os.path.splitext(img_name)[0]

    # Loop through grid rows and columns
    for r in range(ROWS):
        for c in range(COLS):
            # Precision Coordinate Calculation
            # Calculates the theoretical boundaries of each grid cell
            y1 = int(r * (h / ROWS))
            y2 = int((r + 1) * (h / ROWS))
            x1 = int(c * (w / COLS))
            x2 = int((c + 1) * (w / COLS))

            # Crop with specific side margins to remove grid lines
            crop = img[y1 + TOP_MARGIN : y2 - BOTTOM_MARGIN, 
                       x1 + LEFT_MARGIN : x2 - RIGHT_MARGIN]

            # Check if crop resulted in valid image
            if crop.size == 0:
                print(f"Warning: Crop at r{r}c{c} is empty. Reduce margins.")
                continue

            # Construct output filename
            out_name = f"{base_name}_r{r}_c{c}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_name)

            # Save the split image
            cv2.imwrite(out_path, crop)
            count += 1

    print(f"Processed {img_name}: {count} images saved.")

print("Success: Splitting complete!")


# NOTE: The code below appears to be for Google Colab or Jupyter Notebooks
# It deals with downloading a dataset from Roboflow.
# Uncomment and install roboflow via pip to use it.
# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="WHzX5kSbytxfLmlWAEXI")
# project = rf.workspace("jp-icc04").project("train_animal_dectection")
# version = project.version(1)
# dataset = version.download("yolov11")
