# Animal Crossing Detection System 🛤️🦌
> **Automated Wildlife Detection & Alerting for Railway Safety**

This project uses **YOLOv11** (Deep Learning) to detect animals in video feeds (like CCTV on a train track) and provides real-time alerts to prevent accidents.

---

## 🚀 Features
- **Real-Time Detection**: Identifying animals locally on video streams.
- **Web Dashboard**: A clean interface to watch the live feed.
- **Auto-Alerting**: Simulates sending urgent SMS warnings to train operators when an animal is on the track.
- **Portable**: Works on Windows, Mac, and Linux.

---

## 🛠️ Prerequisites
Before running this on your friend's laptop, ensure they have:
1.  **Python 3.8+** installed. (Download from [python.org](https://www.python.org/downloads/)).
2.  **Git** (Optional, to clone the repo, or just copy the folder).

---

## 📦 Installation & Setup (For your Friend)

Follow these steps exactly to run existing code on a new laptop:

### 1. Copy the Code
Copy the entire folder containing these files to the new laptop.

### 2. Open a Terminal
- Open **Command Prompt** (cmd) or **PowerShell** on Windows.
- Navigate to the folder you just copied:
  ```bash
  cd path/to/this/folder
  ```
  *(Tip: You can type `cd`, press space, and drag the folder into the terminal window).*

### 3. Create a Virtual Environment (Recommended)
This keeps your system clean.
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```
*You should see `(.venv)` appear at the start of your command line.*

### 4. Install Dependencies
Run this command to install Flask, YOLO, and other required tools:
```bash
pip install -r requirements.txt
```
*Wait for it to download all libraries.*

---

## ▶️ How to Run

### **Option 1: Run the Web Dashboard (Recommended)**
This starts the full system with the web interface and alerting.

1.  Run the app:
    ```bash
    python app.py
    ```
2.  Once you see `Running on http://127.0.0.1:5000`, open your web browser.
3.  Go to: **http://localhost:5000**
4.  You will see the video feed. Check the terminal window for "ALERT TRIGGERED" messages!

### **Option 2: Run Simple Video Detection**
If you just want to see a pop-up window with detections (no web browser needed):
```bash
python predict_video.py
```

---

## ⚙️ Configuration (Modifying Paths)
**Great news!** The code has been updated to use **Relative Paths**. 
This means **you don't need to change any paths** as long as you keep the files in the same folder structure.

- Ensure `best (1).pt` (The Model) is in the main folder.
- Ensure `animal_slideshow.mp4` (The Video) is in the main folder.

If you want to use a **different video**:
1.  Open `app.py` in a text editor (Notepad, VS Code).
2.  Look for line ~13:
    ```python
    VIDEO_PATH = os.path.join(BASE_DIR, 'new_video_name.mp4')
    ```
3.  Change `'animal_slideshow.mp4'` to your new file name.

---

## 📂 Project Structure
- **app.py**: The main website code (Flask).
- **predict_video.py**: A simpler script to run detection in a pop-up window.
- **best (1).pt**: The "Brain" (Trained YOLO model).
- **templates/index.html**: The design file for the website.
- **requirements.txt**: List of all software libraries needed.

---

### trouble?
- **"Module not found"**: Did you forget to run `pip install -r requirements.txt`?
- **"Model not found"**: Make sure `best (1).pt` is in the folder.
- **Video lagging**: On laptops without a dedicated GPU, detection might be slow. This is normal for Deep Learning!
