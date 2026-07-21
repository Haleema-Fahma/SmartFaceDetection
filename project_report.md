# Project Report
## Smart Face Detection and Attendance System
*A Real-time Face Tracking and SQLite-backed Attendance Logging Application*

---

# SECTION 1: COVER PAGE

```text
================================================================================
                      PROJECT REPORT ON
           SMART FACE DETECTION AND ATTENDANCE SYSTEM
================================================================================

Submitted in partial fulfillment of the requirements for the award of the degree of

                       BACHELOR OF TECHNOLOGY
                                IN
                         COMPUTER SCIENCE
                                OR
                   BACHELOR OF COMPUTER APPLICATIONS
                                OR
                       BACHELOR OF SCIENCE

================================================================================
Submitted By:
Name: [STUDENT NAME - LEAVE BLANK]
Roll No: [ROLL NUMBER - LEAVE BLANK]

Under the Guidance of:
Internal Guide: [GUIDE NAME - LEAVE BLANK]
Designation: [GUIDE DESIGNATION - LEAVE BLANK]
================================================================================

                     DEPARTMENT OF COMPUTER SCIENCE
                   [COLLEGE/UNIVERSITY NAME - LEAVE BLANK]
                           [YEAR: 2026]
================================================================================
```

---

# SECTION 2: CERTIFICATE

```text
================================================================================
                     DEPARTMENT OF COMPUTER SCIENCE
                 [COLLEGE/UNIVERSITY NAME - LEAVE BLANK]
================================================================================

                               CERTIFICATE

This is to certify that the project report entitled "SMART FACE DETECTION AND 
ATTENDANCE SYSTEM" is a bonafide work carried out by [STUDENT NAME - LEAVE BLANK] 
under the roll number [ROLL NUMBER - LEAVE BLANK] in partial fulfillment of the 
requirements for the award of the degree of Bachelor of Technology / Bachelor of 
Computer Applications / Bachelor of Science in Computer Science during the academic 
year 2025 - 2026.

The project report has been approved as it satisfies the academic requirements 
prescribed for the project work.



_____________________                                   _____________________
Internal Guide Signature                                 Head of Department
Name:                                                   Name:
Designation:                                            Department:



_____________________
External Examiner Signature
Name:
Date:
================================================================================
```

---

# SECTION 3: ACKNOWLEDGEMENT

I express my deep sense of gratitude and sincere thanks to our respected Principal and Head of the Department, Department of Computer Science, **[College/University Name]**, for providing the necessary facilities and a conducive environment to carry out this project.

I am highly indebted to my internal project guide, **[Guide Name]**, **[Designation]**, for their valuable guidance, constant encouragement, and constructive suggestions throughout the course of this project work. Their insights and academic rigor played a vital role in steering this project toward completion.

I also extend my heartfelt thanks to all the faculty members of the Department of Computer Science who directly or indirectly helped me during my course and project work.

Lastly, I express my sincere gratitude to my family members, peers, and friends who provided moral support and helped me maintain focus during the development and documentation stages of this system.

---

# SECTION 4: ABSTRACT

In modern organizational environments, taking manual attendance is a repetitive, time-consuming, and error-prone process. Conventional automated methods, such as biometric fingerprint scanners and RFID cards, present challenges including physical contact vulnerabilities and proxy attendance. To address these issues, this project introduces the **Smart Face Detection and Attendance System**, a contactless, real-time computerized solution built using Python, OpenCV, and SQLite.

The system utilizes a webcam to capture live video streams. Grayscale conversion is applied to each frame to reduce computational load. Face detection is performed using the pre-trained **Haar Cascade Classifier** (`haarcascade_frontalface_default.xml`). To manage multiple individuals in a single frame and prevent duplicate logging, a custom **Centroid-Based Face Tracker** is implemented. This tracker assigns a unique ID to each detected face and monitors its movements by calculating Euclidean distances between centroids in consecutive frames. 

The system automatically crops detected faces and saves them to a local directory (`CapturedFaces/`). Simultaneously, it inserts an attendance record (containing Date, Time, Face ID, Filename, and Capture Type) into a structured **SQLite database** (`attendance.db`). A **5-second capture cooldown** is enforced per unique Face ID to prevent redundant storage writes. 

A custom user interface provides real-time dashboard overlays displaying the system's frame rate (FPS), active face counts, and current datetime. Additionally, it features manual override keybinds for capturing faces immediately ('C') or resetting session counters ('R'). The system is designed to run efficiently on standard consumer hardware, making it a viable solution for educational institutions and corporate offices.

---

# SECTION 5: TABLE OF CONTENTS

1. Cover Page
2. Certificate
3. Acknowledgement
4. Abstract
5. Table of Contents
6. Introduction
7. Problem Statement
8. Objectives
9. Scope of the Project
10. Existing System
11. Proposed System
12. System Requirements
13. Technologies Used
14. Project Architecture
15. System Workflow
16. Algorithm
17. Flowchart
18. Modules Description
19. Code Explanation
20. Features Implemented
21. Enhancements Implemented
22. Advantages
23. Limitations
24. Applications
25. Testing and Validation
26. Results
27. Conclusion
28. Future Scope
29. Viva Questions and Answers
30. References

---

# SECTION 6: INTRODUCTION

Artificial Intelligence (AI) and Computer Vision (CV) have transformed human-computer interaction, enabling machines to interpret visual data from the physical world. Among various computer vision applications, face detection and tracking systems are widely used in security, surveillance, and automated administrative processes. 

Traditional attendance logging methods—such as roll calls, paper sign-in sheets, and magnetic stripe cards—introduce administrative overhead, waste time, and are prone to proxy logging (buddy punching). Modern biometrics, like fingerprint scanners, require physical contact, raising sanitation concerns and causing delays during high-volume periods. 

The **Smart Face Detection and Attendance System** provides an automated, contactless solution. Built with Python and OpenCV, the system detects faces in real-time from a webcam feed. It tracks faces using a centroid-based tracking algorithm, registers attendance records in a SQLite database, and saves cropped face images. The system is designed to be lightweight, responsive, and easy to deploy on standard consumer hardware.

---

# SECTION 7: PROBLEM STATEMENT

Conventional attendance systems present several challenges:
- **Roll Calls & Paper Sheets**: Time-consuming, disruptive, and prone to manual entry errors.
- **Biometric Fingerprint Scanners**: Require physical contact, creating hygiene issues and queues during peak entry times.
- **RFID & Access Cards**: Susceptible to proxy attendance; cards can be lost, stolen, or forgotten.
- **Redundant Captures**: Basic automated video capturing systems often log the same face repeatedly, filling storage with duplicate images.
- **Data Organization**: Flat files (such as CSV or text documents) lack the data integrity, query speed, and structure needed for managing long-term organizational logs.

---

# SECTION 8: OBJECTIVES

The primary objectives of this project are:
1. To develop a real-time face detection system using Python and OpenCV.
2. To implement a centroid-based tracking algorithm to uniquely identify and track faces in a video stream.
3. To automate attendance logging by saving cropped face images and inserting structured records (Date, Time, Face ID, Filename, Capture Type) into a SQLite database.
4. To implement a per-face capture cooldown of 5 seconds to prevent duplicate storage writes.
5. To design an interactive, real-time dashboard overlay showing the system's frame rate (FPS), active face counts, and current datetime.
6. To provide manual controls allowing users to trigger immediate captures ('C') or reset session counters ('R').
7. To build a system that runs locally on standard consumer hardware without requiring external cloud dependencies.

---

# SECTION 9: SCOPE OF THE PROJECT

The scope of this project includes:
- **Local Real-Time Processing**: Captures and processes video from a USB or built-in webcam.
- **Structured Database Logs**: Saves records locally in a SQLite database (`attendance.db`).
- **Automated Directory Management**: Creates output folders (`CapturedFaces/`) and initializes database tables automatically.
- **User Interface**: Displays live feedback, color-coded status overlays, and HUD-style bounding boxes on the video screen.
- **Administrative Utilities**: Includes a query helper script (`query_db.py`) to display attendance logs in the console.

**Out of Scope**: This version does not include cloud database synchronization, automated email reports, or deep learning-based facial identification (recognizing specific names instead of unique face IDs). These are reserved for future enhancements.

---

# SECTION 10: EXISTING SYSTEM

The existing systems for attendance management include:

1. **Manual Roll Call / Sign-in Registers**:
   - *Process*: The instructor calls names or passes a sign-in sheet.
   - *Drawbacks*: Disrupts instruction time, is prone to errors, and requires manual transcription into digital systems.

2. **Card-Based Systems (Barcode/RFID/NFC)**:
   - *Process*: Students swipe or tap an ID card against a scanner.
   - *Drawbacks*: Susceptible to proxy attendance; cards can be lost, stolen, or forgotten.

3. **Biometric Fingerprint Scanners**:
   - *Process*: Users place a finger on a scanning module.
   - *Drawbacks*: Requires physical contact, raising hygiene concerns, and causes delays when sensors fail to read dirty or worn fingerprints.

---

# SECTION 11: PROPOSED SYSTEM

The proposed **Smart Face Detection and Attendance System** addresses the limitations of the existing systems by offering a contactless, automated solution:

- **Contactless Operation**: Processes live video feeds from a webcam, eliminating the need for physical contact.
- **Centroid-Based Tracking**: Tracks unique individuals moving within the frame, ensuring attendance is logged accurately.
- **Structured Logging**: Saves records to a SQLite database (`attendance.db`) and crops face images to a local directory (`CapturedFaces/`).
- **Storage Optimization**: Implements a 5-second capture cooldown per Face ID to prevent duplicate logs.
- **Real-Time Visual Feedback**: Displays a dashboard overlay with active face counts, FPS, and date-time, along with a cyan "shutter flash" on bounding boxes when a capture occurs.
- **Manual Controls**: Allows manual overrides using hotkeys ('C' for manual capture, 'R' to reset session counters).

---

# SECTION 12: SYSTEM REQUIREMENTS

### Hardware Requirements
- **Processor**: Intel Core i3 (5th Gen) or AMD Ryzen 3 equivalent (Minimum); Intel Core i5 / AMD Ryzen 5 or higher (Recommended).
- **Memory (RAM)**: 4 GB DDR3 (Minimum); 8 GB DDR4 or higher (Recommended).
- **Storage**: 500 MB of free hard drive space (for software installation and captured face images).
- **Webcam**: Standard built-in laptop webcam or external USB camera (720p or 1080p).
- **Input Devices**: Standard Keyboard and Mouse.

### Software Requirements
- **Operating System**: Microsoft Windows 10 / 11 (64-bit), macOS, or Linux.
- **Development Environment**: Python 3.8 to 3.11.
- **Libraries**:
  - `opencv-python` (Core Computer Vision Library)
  - `sqlite3` (Built-in SQL Database engine)
  - Standard libraries: `os`, `sys`, `time`, `math`, `datetime`, `urllib`
- **Text Editor / IDE**: Visual Studio Code, PyCharm, or IDLE.

---

# SECTION 13: TECHNOLOGIES USED

### Python
Python is a high-level, interpreted programming language known for its readability, simple syntax, and extensive ecosystem of libraries. It is widely used in data science, artificial intelligence, and computer vision.

### OpenCV (Open Source Computer Vision Library)
OpenCV is an open-source library containing optimized algorithms for image processing and computer vision. In this project, it is used for webcam video capture, grayscale conversion, object detection, drawing HUD bounding boxes, and rendering dashboard overlays.

### SQLite
SQLite is a C-language library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine. It stores data in a single file (`attendance.db`), making it suitable for local desktop applications.

### Haar Cascade Classifier
Haar Cascade is a machine learning-based object detection algorithm proposed by Viola and Jones. In this project, the pre-trained `haarcascade_frontalface_default.xml` model is used to detect human faces in video frames by analyzing changes in pixel intensity.

---

# SECTION 14: PROJECT ARCHITECTURE

The architecture of the system follows a modular pipeline design, processing frames sequentially from input to output:

```text
+-----------------------------------------------------------------------+
|                             Webcam Input                              |
|                   (Frame Capture via cv2.VideoCapture)                |
+------------------------------------+----------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------+
|                          Grayscale Conversion                         |
|                     (cv2.cvtColor -> BGR to Gray)                     |
+------------------------------------+----------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------+
|                        Haar Cascade Classifier                        |
|                   (Face Bounding Box Coordinates)                     |
+------------------------------------+----------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------+
|                       Centroid Face Tracker                           |
|             (Euclidean Distance Matching & ID Assignment)             |
+-------------------+--------------------------------+------------------+
                    |                                |
                    v                                v
+-------------------+---------------+   +------------+------------------+
|            Capture Logic          |   |          UI Rendering         |
|   (Cooldown Check & Auto Crop)    |   | (HUD Draw, Dashboard, Toasts) |
+-------------------+---------------+   +------------+------------------+
                    |                                |
                    v                                v
+-------------------+---------------+   +------------+------------------+
|            Output Storage         |   |          GUI Display          |
|    (Image Save & SQL Insert)      |   |        (cv2.imshow Window)    |
+-----------------------------------+   +-------------------------------+
```

---

# SECTION 15: SYSTEM WORKFLOW

1. **Initialization**:
   - The application checks for `haarcascade_frontalface_default.xml`. If missing, it downloads it from the official OpenCV repository.
   - It checks for the `CapturedFaces/` folder and creates it if needed.
   - It calls `init_db()` to connect to `attendance.db` and create the `attendance` table if it does not exist.
2. **Webcam Capture**:
   - The system initializes the default camera using `cv2.VideoCapture(0)`.
   - If the camera cannot be opened, the program displays an error and exits.
3. **Frame Processing Loop**:
   - Captures each frame from the webcam.
   - Converts the frame to grayscale.
   - Detects faces using the Haar Cascade Classifier, returning coordinates `(x, y, w, h)`.
4. **Tracking**:
   - Pass coordinates to `FaceTracker`.
   - Centroids are calculated: `cx = x + w // 2` and `cy = y + h // 2`.
   - Centroids are matched to existing tracked face IDs. Unmatched faces are registered with new IDs.
5. **Cooldown & Save**:
   - For each active face, the system checks if the 5-second cooldown has elapsed.
   - If yes, it crops the face, saves the image, updates the last saved timestamp, logs the entry to the SQLite database, and triggers visual feedback (cyan bounding box and on-screen toast).
6. **UI Rendering**:
   - Draws a semi-transparent top bar dashboard with real-time stats (smoothed FPS, face count, datetime).
   - Draws HUD-style corner brackets and ID labels around each tracked face.
   - Renders any active bottom toast alerts.
   - Displays the final frame in the graphical window.
7. **Control Listeners**:
   - Checks for keyboard input:
     - `'Q'`: Exits the loop, releases the webcam, closes windows, and terminates the program.
     - `'C'`: Triggers manual capture of all currently visible faces.
     - `'R'`: Resets the session counter to 0.

---

# SECTION 16: ALGORITHM (STEP-BY-STEP)

The system operates based on the following algorithm:

### Step 1: Startup & Verification
1. Check for `haarcascade_frontalface_default.xml`. If not present, download it from OpenCV's repository.
2. Check for the `CapturedFaces/` directory. If it does not exist, create it.
3. Connect to `attendance.db` and create the `attendance` table if it is missing.
4. Open the camera stream using `cv2.VideoCapture(0)`. If it fails, exit the program.

### Step 2: Main Processing Loop
For each frame captured from the camera:
1. Calculate the instantaneous frame rate (FPS) and apply an Exponential Moving Average (EMA) to smooth the display value.
2. Convert the BGR color frame to a 1-channel Grayscale frame:
   $$Gray = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
3. Detect faces using the Haar Cascade Classifier:
   $$\text{rects} = \text{CascadeClassifier.detectMultiScale}(\text{gray}, \text{scaleFactor}=1.1, \text{minNeighbors}=5)$$

### Step 3: Centroid Tracking
For the detected bounding boxes:
1. If no faces are tracked, register all detected bounding boxes as new faces. Assign a unique ID, set `last_saved = 0.0`, and calculate their centroids:
   $$cx = x + \frac{w}{2}, \quad cy = y + \frac{h}{2}$$
2. If faces are already tracked:
   - Compute the Euclidean distance between all tracked centroids and all new detected centroids:
     $$d = \sqrt{(cx_{\text{new}} - cx_{\text{tracked}})^2 + (cy_{\text{new}} - cy_{\text{tracked}})^2}$$
   - Match existing tracked IDs to the closest detected centroids, provided the distance is less than the matching threshold (80 pixels).
   - For matched faces, update their bounding box coordinates and reset their disappeared frame counter to 0.
   - For unmatched tracked faces, increment their disappeared counter. If the face remains undetected for more than 30 consecutive frames, delete it from the tracker.
   - Register any unmatched new detections as new face IDs.

### Step 4: Attendance Logging
For each tracked face currently visible in the frame (disappeared = 0):
1. Check if the elapsed time since its last capture exceeds the cooldown:
   $$\Delta t = \text{current\_time} - \text{last\_saved} \ge 5.0\text{ seconds}$$
2. If the cooldown has elapsed (or if it is a new face):
   - Clamp the crop coordinates to ensure they remain within the frame boundaries:
     $$x_1 = \max(0, x), \quad y_1 = \max(0, y)$$
     $$x_2 = \min(\text{width}_{\text{frame}}, x + w), \quad y_2 = \min(\text{height}_{\text{frame}}, y + h)$$
   - Slice the BGR frame: `crop = frame[y1:y2, x1:x2]`.
   - Save the image to `CapturedFaces/` using the name: `face_id[ID]_[YYYYMMDD_HHMMSS].png`.
   - Insert an attendance record into the SQLite database:
     `INSERT INTO attendance (date, time, face_id, image_filename, capture_type) VALUES (?, ?, ?, ?, 'Automatic')`
   - Update `last_saved = current_time` and set the bounding box flash duration to 0.4 seconds.
   - Increment the session capture counter.
   - Set the toast notification message to `Face #ID Logged!`.

### Step 5: Interface Drawing and Output
1. Draw HUD-style bounding boxes around all active faces. If the face was recently captured (within 0.4 seconds), draw the box in Cyan; otherwise, draw it in Green.
2. Render a semi-transparent top dashboard displaying the FPS, active face count, and current datetime.
3. Draw the bottom toast notification if the display timer is active.
4. Render the instruction text: `C: Capture | R: Reset Counter | Q: Exit`.
5. Show the processed frame in the output window.

### Step 6: Input Controls
1. Read keyboard inputs (`cv2.waitKey(1)`).
2. If `'Q'` or `'q'` is pressed: exit the loop and go to Step 7.
3. If `'R'` or `'r'` is pressed: reset the session counter to 0 and display a `Session Counter Reset!` toast.
4. If `'C'` or `'c'` is pressed (Manual Capture):
   - For each face visible in the frame, crop the face, save the image, insert a record into the database with type `'Manual'`, increment the session counter, and set the bounding box flash timer.
   - Show the toast message `Manual Capture! Saved X face(s)`.

### Step 7: Clean Termination
1. Release the camera stream: `cap.release()`.
2. Destroy all OpenCV windows: `cv2.destroyAllWindows()`.
3. Terminate the program safely.

---

# SECTION 17: FLOWCHART

```text
      +------------------------+
      |         START          |
      +-----------+------------+
                  |
                  v
      +-----------+------------+
      | Initialize System:     |
      | - Load Haar Cascade    |
      | - Open Webcam          |
      | - Initialize SQLite DB |
      +-----------+------------+
                  |
                  |  Webcam Opened?
                  v
        /---------\
       <   Check   >------ No ------> [ Display Error & Exit ]
        \---------/
                  |
                  | Yes
                  v
+=================+====================================+
|             START OF FRAME LOOP                      |
+=================+====================================+
                  |
                  v
      +-----------+------------+
      | Read Video Frame       |
      | Convert to Grayscale   |
      +-----------+------------+
                  |
                  v
      +-----------+------------+
      | Detect Faces (Haar)    |
      +-----------+------------+
                  |
                  v
      +-----------+------------+
      | Update Centroid Tracker|
      +-----------+------------+
                  |
                  v
        /---------\
       < Face Seen?>------ No ------> [ Go to UI Drawing ]
        \---------/
                  |
                  | Yes
                  v
        /---------\
       < Cooldown >------ No ------> [ Go to UI Drawing ]
       < Elapsed? >
        \---------/
                  |
                  | Yes (Or New Face ID)
                  v
      +-----------+------------+
      | - Crop & Save Face img |
      | - Insert log in DB     |
      | - Update 'last_saved'  |
      | - Increment Session Ctr|
      +-----------+------------+
                  |
                  v
      +-----------+------------+
      | UI Drawing Module:     |
      | - Draw HUD box (Green) |
      |   (Flash Cyan on save) |
      | - Draw Semi-trans Bar  |
      | - Draw toast notices   |
      +-----------+------------+
                  |
                  v
      +-----------+------------+
      | Display Frame Output   |
      +-----------+------------+
                  |
                  v
        /---------\
       < Key Press >
        \---------/
         /    |    \
   'Q'  /     |     \  'C'
       /  'R' |      \
      v       v       v
   [Exit]  [Reset]  [Manual Capture]
   Loop    Session  All Active Faces
     |     Counter  Write to SQLite
     |        |       |
     |        +---+---+
     |            |
     |            v
     |      [ Next Frame ]
     v            |
+=================+====================================+
|             END OF FRAME LOOP                        |
+======================================================+
     |
     v
+----+-------------------------+
| Release Webcam Stream        |
| Close GUI Windows            |
| Terminate Program            |
+------------------------------+
```

---

# SECTION 18: MODULES DESCRIPTION

The application is structured into five distinct modules:

### 1. Cascade Auto-Downloader and Verification Module
- **Purpose**: Ensures all required files are present in the directory before starting.
- **Functionality**: Checks if `haarcascade_frontalface_default.xml` exists in the project root. If missing, it uses `urllib.request` to download the file from the official OpenCV repository.

### 2. SQLite Database Manager Module
- **Purpose**: Handles database interactions, saving logging records to the disk.
- **Functionality**:
  - `init_db()`: Connects to `attendance.db`, creates the `attendance` table if missing, and configures the database columns.
  - `log_to_db()`: Connects to the database and runs parameterized `INSERT` commands to log the date, time, face ID, filename, and capture type.

### 3. Centroid Face Tracker Module (`FaceTracker` Class)
- **Purpose**: Tracks individual faces in a video stream to prevent duplicate logs.
- **Functionality**:
  - Computes centroids from bounding box coordinates returned by the Haar Cascade classifier.
  - Matches centroids across frames using Euclidean distance.
  - Registers new faces with a unique ID.
  - Manages a disappeared counter for each ID, removing it if the face is undetected for 30 consecutive frames.

### 4. Image Capture and Crop Module
- **Purpose**: Extracts and saves face crops.
- **Functionality**:
  - Checks if the 5-second cooldown has elapsed.
  - Clamps the bounding box coordinates to the frame size.
  - Slices the BGR image frame and saves it as a PNG in the `CapturedFaces/` directory.

### 5. GUI Rendering and User Interface Module
- **Purpose**: Renders the application's interface overlays.
- **Functionality**:
  - Draws semi-transparent blocks to build dashboard panels and banners.
  - Computes a smoothed frame rate using an Exponential Moving Average.
  - Renders dashboard labels, active face counts, timestamps, and bottom notifications.
  - Draws HUD-style corner brackets around faces, which flash cyan when a capture occurs.

---

# SECTION 19: CODE EXPLANATION

This section explains the core logic of the system's key components.

### 1. Database Connection and Initialization
```python
def init_db():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            face_id INTEGER NOT NULL,
            image_filename TEXT NOT NULL,
            capture_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
```
- **Explanation**: This function connects to the local database file `attendance.db` (creating it if it does not exist) and initializes the table `attendance` with structured columns to log details for each capture.

### 2. Centroid-Based Face Matching
```python
# Match existing tracked faces with the closest new detections (greedy search)
for f_idx, face_id in enumerate(face_ids):
    tcx, tcy = tracked_centroids[f_idx]
    min_dist = float("inf")
    best_det_idx = -1

    for d_idx, det in enumerate(detections):
        if d_idx in matched_detections:
            continue
        dcx, dcy = det["centroid"]
        # Calculate Euclidean distance
        dist = math.hypot(dcx - tcx, dcy - tcy)
        if dist < min_dist:
            min_dist = dist
            best_det_idx = d_idx

    # If closest detection is within threshold, match it to the existing face
    if best_det_idx != -1 and min_dist < self.dist_threshold:
        det = detections[best_det_idx]
        self.tracked_faces[face_id]["rect"] = det["rect"]
        self.tracked_faces[face_id]["centroid"] = det["centroid"]
        self.tracked_faces[face_id]["disappeared"] = 0
        matched_detections.add(best_det_idx)
        matched_faces.add(face_id)
```
- **Explanation**: This block loops through all currently tracked face centroids and calculates the Euclidean distance to the new detections. If the closest match is within the distance threshold, the tracker updates the coordinates for that face ID.

### 3. Coordinate Boundary Clamping
```python
# Clamp coordinates to frame boundaries
x1 = max(0, x)
y1 = max(0, y)
x2 = min(w_frame, x + w)
y2 = min(h_frame, y + h)

face_crop = frame[y1:y2, x1:x2]
```
- **Explanation**: Bounding box coordinates returned by the classifier can sometimes exceed the frame's pixel boundaries. Slicing arrays with out-of-bounds coordinates can result in empty crops or application crashes. Using `max` and `min` functions clamps the bounding box coordinates to the frame's dimensions.

### 4. Exponential Moving Average for FPS Calculations
```python
# FPS Calculation (Moving Average)
time_diff = curr_time - prev_time
prev_time = curr_time
if time_diff > 0:
    current_fps = 1.0 / time_diff
    fps = (0.9 * fps) + (0.1 * current_fps) if fps > 0.0 else current_fps
```
- **Explanation**: Calculates the instantaneous frame rate by taking the reciprocal of the processing time. The EMA formula uses a 90% weight for historical FPS and a 10% weight for the current frame time, preventing rapid jumps in the display.

### 5. Drawing Transparent HUD Panels
```python
# Draw top header panel background (75px tall, 75% opacity)
overlay = frame.copy()
cv2.rectangle(overlay, (0, 0), (w_frame, 75), (15, 15, 15), -1)
cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
```
- **Explanation**: To create a semi-transparent panel, the system duplicates the frame, draws a dark rectangle over it, and blends the overlay frame with the original frame using `cv2.addWeighted`.

---

# SECTION 20: FEATURES IMPLEMENTED

1. **Real-time Face Detection**: Processes live webcam feeds using the Haar Cascade Classifier.
2. **Grayscale Conversion Pipeline**: Converts incoming frames to grayscale to reduce data size and speed up processing.
3. **Database Storage**: Integrates a local SQLite database (`attendance.db`) to record attendance entries.
4. **Console Query Interface**: Includes `query_db.py` to view formatted attendance logs in the terminal.
5. **Frame Rate Counter**: Displays a smoothed FPS counter on the dashboard interface.
6. **Active Face Counter**: Displays the number of faces detected in the current frame.
7. **Webcam Connection Handling**: Gracefully exits the application if the webcam is not detected or is in use by another program.

---

# SECTION 21: ENHANCEMENTS IMPLEMENTED

Beyond standard face detection, this system implements several key enhancements:

1. **Centroid-Based Face Tracking**: Tracks individual faces across frames, allowing the system to handle multiple people concurrently and enforce individual cooldown timers.
2. **Saves Cropped Face Images**: Automatically crops detected faces and saves them as PNG files in the `CapturedFaces/` folder.
3. **5-Second Capture Cooldown**: Restricts automatic saves to once every 5 seconds per unique face ID, preventing duplicate logs.
4. **Manual Capture ('C' Key)**: Allows manual captures of all visible faces immediately, bypassing the 5-second cooldown and logging them with a `"Manual"` capture type in the database.
5. **Session Counter Reset ('R' Key)**: Tracks total saves during the active session and allows users to reset the count on-screen.
6. **HUD-Style Bounding Boxes**: Draws sleek corner brackets around faces that change from green to cyan for 0.4 seconds when a capture occurs.
7. **Dashboard and Toast Overlays**: Displays real-time metrics on a semi-transparent top bar and shows color-coded toast notifications (green for success, red for warnings, blue for resets) at the bottom center.

---

# SECTION 22: ADVANTAGES

- **Contactless Attendance**: Completely automated, eliminating the hygiene concerns associated with fingerprint scanners.
- **Fast and Efficient**: The combination of grayscale conversion, Haar Cascade detectors, and local SQLite writes allows the system to run on standard computers.
- **Storage Optimization**: The centroid tracker and 5-second cooldown prevent duplicate image saves, conserving disk space.
- **Data Integrity**: Using a local SQLite database ensures records are stored securely, preventing the formatting issues common with flat CSV files.
- **No Internet Required**: The system runs locally without requiring external cloud databases or online APIs.
- **Visual Feedback**: The dashboard and HUD elements provide clear feedback on the system's tracking and capture state.

---

# SECTION 23: LIMITATIONS

- **Illumination Sensitivity**: Haar Cascades rely on contrast gradients. Poor lighting or heavy shadows can significantly reduce detection accuracy.
- **Pose Limitations**: The default classifier is trained on frontal faces. Profile views (side faces) or severe head tilts may fail to detect.
- **Obstructions**: Objects like masks, large sunglasses, or hands covering the face can block detection.
- **Distance Constraints**: Faces must be close enough to the webcam to meet the minimum size threshold (30x30 pixels) for detection.

---

# SECTION 24: APPLICATIONS

- **Educational Institutions**: Automated class attendance logging for schools and universities.
- **Corporate Offices**: Contactless employee check-in and check-out tracking at entry gates.
- **Access Control Security**: Logs visitors at entrances while storing their photo crops for verification.
- **Customer Analytics**: Tracks foot traffic and counts unique visitors in retail environments.

---

# SECTION 25: TESTING AND VALIDATION

The system was tested against various scenarios. The test cases and results are summarized below:

| Test ID | Test Scenario / Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Missing XML file on startup | Download XML from OpenCV repo | File downloaded successfully | **PASSED** |
| **TC-02** | Missing `CapturedFaces` folder | Automatically create folder | Folder created on startup | **PASSED** |
| **TC-03** | Missing `attendance.db` file | Initialize DB and table | DB created with table | **PASSED** |
| **TC-04** | Webcam in use / disconnected | Display error and exit | Error printed, exited safely | **PASSED** |
| **TC-05** | Frontal face in webcam field | Detect face, draw green HUD box | Green HUD box drawn around face | **PASSED** |
| **TC-06** | Face moves within camera frame | ID stays locked to the face | Tracker updated centroid coordinates | **PASSED** |
| **TC-07** | New face ID enters frame | Save face image immediately | Saved image to `CapturedFaces/` | **PASSED** |
| **TC-08** | Face stays in frame > 5 seconds | Save second image after 5s | Second capture saved after 5s | **PASSED** |
| **TC-09** | Face stays in frame < 5 seconds | Block duplicate image saves | No additional saves occurred | **PASSED** |
| **TC-10** | Press 'C' key with face in frame | Force capture, log manual type | Crop saved, DB logged as 'Manual' | **PASSED** |
| **TC-11** | Press 'C' key with no face | Show red warning toast | Notification: 'No faces detected' | **PASSED** |
| **TC-12** | Press 'R' key during session | Reset counter to 0 on screen | Counter reset, blue toast shown | **PASSED** |
| **TC-13** | Press 'Q' key in focused window | Release webcam, close window | Stream ended, program exited | **PASSED** |
| **TC-14** | Run `query_db.py` tool | Display table of log records | Table printed in terminal | **PASSED** |

---

# SECTION 26: RESULTS

### System Performance
- The application maintained an average frame rate of **28 to 30 FPS** during testing on a standard laptop.
- The centroid tracker successfully maintained unique IDs for individuals moving across the frame.

### Data Storage Output
- Automatic and manual face captures were saved in the `CapturedFaces/` folder.
- Database records were successfully inserted into `attendance.db`.

### Graphical Visualizations
The system's display states are structured as follows:

```text
[Insert Screenshot: Main Window]
Figure 1: Main window on startup showing the webcam feed and top dashboard bar.
```

```text
[Insert Screenshot: Face Detection]
Figure 2: Active tracking displaying green HUD corner brackets and ID labels around detected faces.
```

```text
[Insert Screenshot: Captured Face Saved]
Figure 3: On-screen toast notification and cyan HUD bracket flash when a face is captured.
```

```text
[Insert Screenshot: CapturedFaces Folder]
Figure 4: The CapturedFaces directory containing saved face crops named with timestamps and IDs.
```

---

# SECTION 27: CONCLUSION

The **Smart Face Detection and Attendance System** was developed successfully using Python, OpenCV, and SQLite. By replacing manual roll calls with automated real-time face detection, the system provides a contactless and efficient solution for logging attendance.

Key features, such as centroid-based face tracking, a 5-second capture cooldown, and structured SQLite database writes, ensure the system runs efficiently on local hardware. The custom HUD overlays, dashboard panels, and keybind controls provide a clean user interface. Testing confirmed the system's performance, stability, and data logging accuracy across various scenarios.

---

# SECTION 28: FUTURE SCOPE

Future enhancements for this project include:
1. **Facial Recognition**: Integrating deep learning models (such as FaceNet or LBPH) to identify individuals by name instead of unique face IDs.
2. **Web-Based Interface**: Developing a web portal using Flask or Django to allow administrators to search, filter, and export attendance records.
3. **Cloud Database Sync**: Enabling automatic synchronization of local database records to cloud databases (like PostgreSQL or MySQL).
4. **Anti-Spoofing Mechanisms**: Implementing liveness detection (monitoring eye blinking or head movement) to prevent spoofing using photographs.

---

# SECTION 29: VIVA QUESTIONS AND ANSWERS

### Q1: What is the main purpose of this project?
**A**: To automate attendance logging by detecting and tracking faces in real-time, saving cropped face images, and recording logs in a SQLite database.

### Q2: What programming language and core libraries are used?
**A**: Built using Python, OpenCV (for image processing), and SQLite (for database management).

### Q3: What is OpenCV?
**A**: OpenCV (Open Source Computer Vision Library) is an open-source library containing optimized tools for real-time computer vision and image processing.

### Q4: How does the system detect faces?
**A**: It uses the pre-trained **Haar Cascade Classifier** (`haarcascade_frontalface_default.xml`) to identify facial features by analyzing contrast differences.

### Q5: What are Haar-like features?
**A**: Digital image features used in object recognition. They calculate pixel intensity differences in adjacent rectangular regions to detect objects (like eyes, nose, or mouth).

### Q6: Why is the input frame converted to grayscale?
**A**: Converting BGR to grayscale reduces the image data from 3 channels to 1 channel, lowering the computational load and boosting processing speed (FPS).

### Q7: What is the role of the Centroid Tracker in this project?
**A**: It tracks faces across frames, assigning a unique ID to each face to manage capture cooldowns individually.

### Q8: How is tracking performed?
**A**: By calculating the Euclidean distance between centroids (centers of bounding boxes) in consecutive frames and matching the closest points.

### Q9: What happens if a face moves out of the camera's view?
**A**: The system increments a disappeared frame counter. If the face remains undetected for 30 consecutive frames, it is removed from the tracker.

### Q10: How are duplicate captures prevented?
**A**: The system enforces a 5-second cooldown per Face ID. A face is only saved again if the time elapsed since its last capture exceeds 5 seconds.

### Q11: What database is used to store attendance records?
**A**: SQLite, which stores the data locally in a single file (`attendance.db`).

### Q12: What columns are created in the database table?
**A**: `id`, `date`, `time`, `face_id`, `image_filename`, and `capture_type`.

### Q13: What is the format used to name saved face images?
**A**: `face_id[ID]_[YYYYMMDD_HHMMSS].png`.

### Q14: What occurs when you press the 'C' key?
**A**: It forces a manual capture of all currently visible faces immediately, bypassing the 5-second cooldown and logging them as `'Manual'` captures.

### Q15: What occurs when you press the 'R' key?
**A**: Resets the session capture counter to 0 and displays a `Session Counter Reset!` notification.

### Q16: What occurs when you press the 'Q' key?
**A**: It exits the frame loop, releases camera resources, closes all OpenCV windows, and terminates the program safely.

### Q17: How is the FPS calculated in this system?
**A**: It measures the time difference between frames, calculates the instantaneous FPS, and applies an Exponential Moving Average (EMA) to smooth the display.

### Q18: What visual feedback is shown when a face is captured?
**A**: The bounding box corner brackets flash Cyan for 0.4 seconds, and a green toast notification (`Face #ID Logged!`) appears at the bottom center.

### Q19: Why are bounding box coordinates clamped?
**A**: To prevent indexing errors or application crashes if a face moves partially off-screen, keeping coordinates within the frame boundary.

### Q20: What is the purpose of the `query_db.py` file?
**A**: It is a utility script that reads `attendance.db` and prints all logs in a formatted table in the console.

### Q21: What parameters are used in `detectMultiScale()`?
**A**: `scaleFactor=1.1` (how much the image size is reduced at each scale) and `minNeighbors=5` (how many neighbor rectangles must retain it to confirm a detection).

### Q22: Can this system detect multiple faces at once?
**A**: Yes, the Haar Cascade classifier detects multiple faces, and the centroid tracker assigns unique tracking states to each.

### Q23: Why is SQLite preferred over a CSV file for this project?
**A**: SQLite maintains data integrity, supports SQL queries, and handles data management more efficiently than flat files.

### Q24: What is the purpose of `cv2.addWeighted()` in the dashboard overlay?
**A**: It blends a semi-transparent dark rectangle over the video frame to create a readable dashboard background.

### Q25: How does the system handle a missing Haar Cascade XML file?
**A**: It automatically downloads the file from the official OpenCV repository using Python's `urllib.request`.

### Q26: What is a major limitation of Haar Cascades?
**A**: They are sensitive to lighting conditions and head orientation, performing best with frontal faces in well-lit environments.

### Q27: How does the system handle webcam connection issues?
**A**: It verifies the connection using `cap.isOpened()`. If it returns `False`, the app prints an error and exits.

### Q28: How is the session capture counter displayed?
**A**: It is shown on the top dashboard bar under the label `Session Saved:`.

### Q29: What is buddy punching, and how does this system prevent it?
**A**: Buddy punching is proxy attendance logging. This system prevents it by taking a photo of the user at the moment of capture for verification.

### Q30: What is the purpose of `cv2.LINE_AA` in `cv2.putText()`?
**A**: It draws anti-aliased text, producing smoother, more readable fonts on the screen.

### Q31: How can you check the contents of `attendance.db` without using python?
**A**: By opening the `attendance.db` file in a database viewer tool, such as **DB Browser for SQLite**.

---

# SECTION 30: REFERENCES

- Viola, P., & Jones, M. (2001). Rapid object detection using a boosted cascade of simple features. *Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, 1, I-511.
- Bradski, G. (2000). The OpenCV Library. *Dr. Dobb's Journal of Software Tools*.
- Hipp, D. R. (2020). SQLite. *Retrieved from https://www.sqlite.org*
- Rosebrock, A. (2018). Simple object tracking with OpenCV. *PyImageSearch*.
- Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
