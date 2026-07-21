# Smart Face Detection and Attendance System

A professional, real-time **Face Detection and Attendance Logging** system built with Python, OpenCV, and SQLite.

> Built as a college project (B.Tech / BCA / B.Sc Computer Science)

---

## Demo

[Insert Screenshot: Main Window]  
*Figure 1: Real-time webcam feed with HUD overlays and dashboard.*

[Insert Screenshot: Face Detection]  
*Figure 2: Green HUD corner brackets and Face ID label on detected face.*

[Insert Screenshot: Captured Face Saved]  
*Figure 3: Cyan bracket flash and toast notification on capture.*

---

## Features

- **Real-Time Face Detection** using Haar Cascade Classifier
- **Centroid-Based Face Tracker** — tracks unique faces with individual IDs
- **SQLite Attendance Log** — auto-creates `attendance.db` with structured records
- **5-Second Capture Cooldown** per face to prevent duplicate logs
- **Cropped Face Image Saving** to `CapturedFaces/` folder
- **Professional HUD Dashboard** — FPS, Face Count, Date & Time overlays
- **Manual Capture** — Press `C` to instantly save all visible faces
- **Session Counter Reset** — Press `R` to reset session capture counter
- **Auto-Download** of Haar Cascade XML if missing
- **Query Utility** — `query_db.py` to print attendance logs in the console

---

## Project Structure

```text
SmartFaceDetection/
│
├── app.py                             # Main application
├── query_db.py                        # Console attendance log viewer
├── requirements.txt                   # Python dependencies
├── haarcascade_frontalface_default.xml # Pre-trained face detector model
├── project_report.md                  # Full college project report
├── README.md                          # This file
├── .gitignore
├── attendance.db                      # (Auto-created) SQLite database
└── CapturedFaces/                     # (Auto-created) Saved face images
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/SmartFaceDetection.git
cd SmartFaceDetection
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note**: `sqlite3` is built into Python — no extra installation needed.

---

## How to Run

```bash
python app.py
```

### Keyboard Controls
| Key | Action |
|-----|--------|
| `C` | Manually capture all visible faces immediately |
| `R` | Reset the session capture counter to 0 |
| `Q` | Safely exit and release webcam |

---

## Viewing Attendance Logs

After running the app, query your attendance database:
```bash
python query_db.py
```

Sample output:
```text
==========================================================================================
ID    | Date         | Time       | Face ID  | Filename                            | Type      
==========================================================================================
1     | 2026-07-21   | 09:55:00   | 0        | face_id0_20260721_095500.png        | Automatic 
2     | 2026-07-21   | 09:55:12   | 0        | face_id0_manual_20260721_095512.png | Manual    
==========================================================================================
Total Logged Records: 2
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| OpenCV (`cv2`) | Webcam capture, face detection, UI drawing |
| Haar Cascade Classifier | Pre-trained frontal face detector |
| SQLite (`sqlite3`) | Local structured attendance database |

---

## System Requirements

- Python 3.8 or higher
- Webcam (built-in or USB)
- Windows / macOS / Linux

---

## License

This project is for educational purposes.

---

## Author

HALEEMA FAHMA M C 
RAJAGIRI COLLEGE OF SOCIAL SCIENCES 
2025-27
