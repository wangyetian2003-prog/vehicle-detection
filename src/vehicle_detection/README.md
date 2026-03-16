# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:** [Wang Yetian] | **Student ID:** [22103334d] | **Date:** March 2026

---

## 1. Overview

This project implements a ROS-based vehicle detection pipeline that reads image frames from a rosbag file, performs real-time vehicle detection using YOLOv8, and displays the results with bounding boxes, class labels, confidence scores, and detection statistics via an OpenCV visualisation UI.

---

## 2. Detection Method

**Model:** YOLOv8n (You Only Look Once, version 8 — nano variant)

YOLOv8 was selected for the following reasons:
- **Speed:** The nano variant runs in real time on CPU, making it suitable for onboard drone deployment where computational resources are limited.
- **Accuracy:** YOLOv8 achieves strong detection performance on the COCO dataset, which includes vehicle classes such as car, truck, bus, and motorcycle.
- **Ease of integration:** The `ultralytics` Python library provides a simple API that integrates cleanly with ROS Noetic and OpenCV.
- **Pre-trained weights:** No custom training is required; the COCO-pretrained model already covers all relevant vehicle classes.

Compared to alternatives such as Faster R-CNN (too slow for real-time use) or SSD (lower accuracy), YOLOv8n offers the best balance of speed and accuracy for this application.

---

## 3. Repository Structure
```
vehicle_detection/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── detect.launch
├── scripts/
│   ├── extract_frames.py
│   ├── detect_vehicles.py
│   └── visualise_ui.py
├── data/
│   └── 2026-02-02-17-57-27.bag
└── README.md
```

---

## 4. Prerequisites

| Requirement | Version |
|---|---|
| OS | Ubuntu 20.04 (WSL2) |
| ROS | Noetic |
| Python | 3.8 |
| ultralytics (YOLOv8) | ≥ 8.0 |
| OpenCV (with GUI) | ≥ 4.2 |
| numpy | ≥ 1.21 |

Install Python dependencies:
```bash
pip install ultralytics opencv-python numpy
```

---

## 5. How to Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/[your-username]/vehicle_detection.git
cd ~/catkin_ws/src
```

**Step 2 — Install dependencies**
```bash
pip install ultralytics opencv-python numpy
sudo apt-get install ros-noetic-cv-bridge
```

**Step 3 — Build the ROS package**
```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

**Step 4 — Place the rosbag file**

Place your `.bag` file in the `data/` folder:
```bash
cp /path/to/your.bag ~/catkin_ws/src/vehicle_detection/data/2026-02-02-17-57-27.bag
```

**Step 5 — Launch the pipeline**
```bash
roslaunch vehicle_detection detect.launch
```

The OpenCV window titled **"Vehicle Detection - AAE4011"** will appear, showing detection results in real time. Press `ESC` to exit.

---

## 6. Sample Results

**Image Extraction Summary:**
- Rosbag file: `2026-02-02-17-57-27.bag`
- Duration: ~114 seconds
- Image topic: `/camera/image_raw/compressed`
- Approximate frame count: ~3400 frames

**Detection Statistics:**
- Detected classes: car, truck, bus, motorcycle
- YOLOv8n model: COCO pretrained
- Real-time display with bounding boxes, class labels, confidence scores, and per-frame vehicle count shown in the top-left overlay

---

## 7. Video Demonstration

**Video Link:** [YouTube (Unlisted)](https://youtu.be/10Hd10kjgFE)

The video demonstrates:
- (a) Launching the ROS package using `roslaunch vehicle_detection detect.launch`
- (b) The OpenCV UI displaying live detection results on rosbag images
- (c) A brief verbal explanation of the detection results and pipeline

---

## 8. Reflection & Critical Analysis

### (a) What Did You Learn?

Through this assignment, I gained two key technical skills.

First, I developed practical experience with **ROS Noetic publisher/subscriber architecture**. I learned how to build a multi-node pipeline where one node plays back a rosbag, a second node subscribes to the image topic and runs inference, and a third node subscribes to the detection results and renders them in a UI. Understanding how ROS topics and message types (particularly `CompressedImage` and `String`) work in practice was significantly more involved than the theoretical understanding from lectures.

Second, I gained hands-on experience with **deploying a deep learning model in a robotics pipeline**. Integrating YOLOv8 via the `ultralytics` library into a ROS node required careful handling of image format conversion between ROS messages and NumPy arrays, managing inference latency relative to the rosbag playback rate, and handling edge cases such as time synchronisation errors (`ROSTimeMovedBackwardsException`).

### (b) How Did You Use AI Tools?

I used Claude (Anthropic) as an AI assistant throughout this assignment. The AI was helpful for generating boilerplate ROS node code, debugging error messages quickly (such as the `IndentationError` and `ROSTimeMovedBackwardsException` issues), and suggesting fixes for environment configuration problems in WSL2.

However, AI tools have clear limitations. The generated code sometimes had structural errors that required manual correction, and the AI occasionally suggested commands that did not match my specific file structure (e.g., wrong launch file names). This highlights that AI assistants are productivity tools, not replacements for understanding — every suggestion required verification and contextual judgement. I made sure to understand each part of the code before submitting.

### (c) How to Improve Accuracy?

**Strategy 1 — Fine-tune YOLOv8 on UAV aerial imagery.**
The COCO-pretrained YOLOv8n model was trained predominantly on ground-level camera images. Aerial images from a drone have a very different perspective (top-down or oblique), smaller object scales, and different lighting conditions. Fine-tuning the model on a UAV-specific dataset such as VisDrone would directly improve detection accuracy for this deployment context.

**Strategy 2 — Use a larger YOLOv8 variant (e.g., YOLOv8s or YOLOv8m).**
The nano variant was chosen for speed, but it sacrifices accuracy. Upgrading to the small or medium variant increases model capacity and improves detection of small or partially occluded vehicles, at the cost of higher computational load. On a platform with a dedicated GPU or edge accelerator (e.g., NVIDIA Jetson), this trade-off is acceptable.

### (d) Real-World Challenges

**Challenge 1 — Computational constraints on embedded hardware.**
A real drone typically uses an embedded computer such as a Raspberry Pi or NVIDIA Jetson. Running YOLOv8 inference at 30 FPS on CPU is not feasible on low-power hardware. The pipeline would need to be optimised using model quantisation (INT8), TensorRT acceleration, or by reducing the inference resolution, all of which introduce accuracy trade-offs that must be carefully managed.

**Challenge 2 — Sensor noise and motion blur.**
In a real flight scenario, the camera image is subject to vibration from rotors, motion blur at high speeds, and variable lighting (glare, shadows). These factors degrade detection confidence significantly compared to the relatively clean rosbag data used in this assignment. Mitigation strategies include hardware vibration dampening, camera exposure tuning, and applying image stabilisation pre-processing before inference.

---

## 9. References

- Ultralytics YOLOv8: https://github.com/ultralytics/ultralytics
- ROS Noetic Documentation: https://wiki.ros.org/noetic
- COCO Dataset: https://cocodataset.org
- VisDrone Dataset: https://github.com/VisDrone/VisDrone-Dataset
- OpenCV Python: https://docs.opencv.org

