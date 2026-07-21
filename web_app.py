"""
Smart Face Detection and Attendance System - Flask Web Application
==================================================================
Flask backend that:
  - Receives webcam frames from the browser as base64 JPEG
  - Runs Haar Cascade face detection using OpenCV
  - Logs attendance records to a local SQLite database
  - Serves the live detection page and attendance dashboard
  - Saves cropped face images to the CapturedFaces/ directory

Author: Senior Python & OpenCV Developer
"""

import os
import sys
import sqlite3
import base64
import numpy as np
import urllib.request
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import cv2

# ==========================================
# 1. FLASK APP INITIALIZATION
# ==========================================
app = Flask(__name__)
CORS(app)

# ==========================================
# 2. CONSTANTS
# ==========================================
CASCADE_FILENAME = "haarcascade_frontalface_default.xml"
CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
OUTPUT_DIR = "CapturedFaces"
DB_FILENAME = "attendance.db"

# ==========================================
# 3. AUTO-DOWNLOAD CASCADE FILE
# ==========================================
def download_cascade_if_missing():
    """Downloads the Haar Cascade XML if not present in project root."""
    if not os.path.exists(CASCADE_FILENAME):
        print(f"[INFO] Downloading {CASCADE_FILENAME}...")
        try:
            urllib.request.urlretrieve(CASCADE_URL, CASCADE_FILENAME)
            print("[SUCCESS] Cascade downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download cascade: {e}")
            sys.exit(1)

# ==========================================
# 4. SQLITE DATABASE FUNCTIONS
# ==========================================
def init_db():
    """Creates the attendance database and table if they don't exist."""
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
    print(f"[DATABASE] Initialized '{DB_FILENAME}' successfully.")

def log_to_db(image_filename, face_id, capture_type="Automatic"):
    """Inserts an attendance record into the SQLite database."""
    now = datetime.now()
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (date, time, face_id, image_filename, capture_type)
            VALUES (?, ?, ?, ?, ?)
        """, (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), face_id, image_filename, capture_type))
        conn.commit()
        conn.close()
        print(f"[DATABASE] Logged Face ID {face_id} ({capture_type}).")
    except Exception as e:
        print(f"[ERROR] DB write failed: {e}")

# ==========================================
# 5. STARTUP: INITIALIZE EVERYTHING
# ==========================================
download_cascade_if_missing()
os.makedirs(OUTPUT_DIR, exist_ok=True)
init_db()

# Load the Haar Cascade Classifier once at startup
face_cascade = cv2.CascadeClassifier(CASCADE_FILENAME)
if face_cascade.empty():
    print("[ERROR] Failed to load Haar Cascade Classifier.")
    sys.exit(1)

print("[INFO] Flask server is ready.")

# ==========================================
# 6. ROUTES
# ==========================================

@app.route('/')
def index():
    """Serves the main live detection page."""
    return render_template('index.html')

@app.route('/attendance')
def attendance_page():
    """Serves the attendance log dashboard page."""
    return render_template('attendance.html')

@app.route('/api/attendance')
def get_attendance():
    """Returns all attendance records as JSON for the dashboard."""
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, time, face_id, image_filename, capture_type
            FROM attendance ORDER BY id DESC
        """)
        records = cursor.fetchall()
        conn.close()
        return jsonify([{
            "id": r[0], "date": r[1], "time": r[2],
            "face_id": r[3], "image_filename": r[4], "capture_type": r[5]
        } for r in records])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/detect', methods=['POST'])
def detect():
    """
    Receives a base64 JPEG frame from the browser.
    Runs Haar Cascade face detection.
    Returns detected bounding boxes as JSON.
    """
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"faces": [], "count": 0, "error": "No image"}), 400

    try:
        # Strip base64 header if present (e.g. "data:image/jpeg;base64,...")
        img_str = data['image']
        if ',' in img_str:
            img_str = img_str.split(',')[1]

        # Decode base64 → NumPy array → OpenCV image
        img_bytes = base64.b64decode(img_str)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"faces": [], "count": 0, "error": "Invalid image"}), 400

        # Convert to grayscale for Haar Cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        face_list = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces]
        return jsonify({"faces": face_list, "count": len(face_list)})

    except Exception as e:
        return jsonify({"faces": [], "count": 0, "error": str(e)}), 500

@app.route('/save_face', methods=['POST'])
def save_face():
    """
    Receives a full frame + face bounding box + face_id.
    Crops the face region, saves as PNG, and logs to SQLite.
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data"}), 400

    try:
        img_str = data.get('image', '')
        face_id = int(data.get('face_id', 0))
        capture_type = data.get('capture_type', 'Automatic')
        region = data.get('face_region', None)

        # Decode the image
        if ',' in img_str:
            img_str = img_str.split(',')[1]
        img_bytes = base64.b64decode(img_str)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None and region:
            x, y, w, h = int(region['x']), int(region['y']), int(region['w']), int(region['h'])
            fh, fw = frame.shape[:2]

            # Clamp coordinates to frame boundaries
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(fw, x + w), min(fh, y + h)
            crop = frame[y1:y2, x1:x2]

            if crop.size > 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
                prefix = "manual_" if capture_type == "Manual" else ""
                filename = f"face_id{face_id}_{prefix}{timestamp}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)

                cv2.imwrite(filepath, crop)
                log_to_db(filename, face_id, capture_type)
                return jsonify({"success": True, "filename": filename})

        return jsonify({"success": False, "error": "Could not crop face"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/CapturedFaces/<filename>')
def captured_face_image(filename):
    """Serves saved cropped face images."""
    return send_from_directory(OUTPUT_DIR, filename)

# ==========================================
# 7. RUN THE SERVER
# ==========================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
