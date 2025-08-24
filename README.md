# Object Tracking with Euclidean Distance (OpenCV)

This project demonstrates **object tracking** in a video using OpenCV and a simple **Euclidean distance tracker**.  
It detects moving objects with background subtraction, assigns each object an ID, and tracks their movement frame by frame.

---

## 📌 Features
- Detects moving objects in a video using `cv2.createBackgroundSubtractorMOG2`.
- Tracks objects across frames using **Euclidean distance** between object centers.
- Assigns a **unique ID** to each detected object.
- Displays bounding boxes and IDs for each tracked object in the video.

---

## 🛠️ Requirements
- Python 3.x
- OpenCV (`cv2`)
- Math library (built-in)

Install OpenCV if you don’t have it:
```bash
pip install opencv-python
