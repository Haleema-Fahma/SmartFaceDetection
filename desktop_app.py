"""
Smart Face Detection and Attendance System (SQLite Database Edition)
======================================================================
A professional Python application that detects faces in real-time,
tracks them, logs attendance records into a SQLite database, and counts
session saves. Includes custom keybinds for manual capture ('C') and
session reset ('R').

Author: Senior Python & OpenCV Developer
"""

import os
import sys
import time
import math
import sqlite3
import urllib.request
from datetime import datetime
import cv2

# ==========================================
# 1. CONSTANTS AND CONFIGURATION
# ==========================================
CASCADE_FILENAME = "haarcascade_frontalface_default.xml"
CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
OUTPUT_DIR = "CapturedFaces"
DB_FILENAME = "attendance.db"
COOLDOWN_SECONDS = 5.0  # Cooldown between captures for the same tracked face

# ==========================================
# 2. AUTO-DOWNLOAD CASCADE FILE
# ==========================================
def download_cascade_if_missing():
    """Downloads the Haar Cascade XML file from OpenCV repository if it's missing."""
    if not os.path.exists(CASCADE_FILENAME):
        print(f"[INFO] '{CASCADE_FILENAME}' not found in the project root.")
        print(f"[INFO] Downloading from the official OpenCV repository...")
        try:
            def progress(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\rDownloading: {percent}%")
                sys.stdout.flush()
                
            urllib.request.urlretrieve(CASCADE_URL, CASCADE_FILENAME, progress)
            print("\n[SUCCESS] Download completed.")
        except Exception as e:
            print(f"\n[ERROR] Failed to download the cascade file: {e}")
            print("[INFO] Please download the file manually and place it in the same directory.")
            sys.exit(1)

# ==========================================
# 3. SQLITE DATABASE LOGGER
# ==========================================
def init_db():
    """Initializes the SQLite database and creates the attendance table if it doesn't exist."""
    try:
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
        print(f"[DATABASE] Initialized SQLite database '{DB_FILENAME}' successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        sys.exit(1)

def log_to_db(image_filename, face_id, capture_type="Automatic"):
    """Inserts a new attendance record into the SQLite database."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (date, time, face_id, image_filename, capture_type)
            VALUES (?, ?, ?, ?, ?)
        """, (date_str, time_str, face_id, image_filename, capture_type))
        conn.commit()
        conn.close()
        print(f"[DATABASE] Logged Face ID {face_id} to DB ({capture_type}).")
    except Exception as e:
        print(f"[ERROR] Failed to write attendance to database: {e}")

# ==========================================
# 4. CENTROID-BASED FACE TRACKER CLASS
# ==========================================
class FaceTracker:
    """
    A simple centroid tracker to uniquely identify faces in video frames.
    Allows us to maintain state (such as cooldown and flash indicators) per individual face.
    """
    def __init__(self, max_disappeared=30, dist_threshold=80):
        self.next_id = 0
        # Stores face details: face_id -> {"rect": (x,y,w,h), "centroid": (cx,cy), "disappeared": int, "last_saved": float, "flash_expiry": float}
        self.tracked_faces = {}
        self.max_disappeared = max_disappeared  # Frames to wait before deleting a face
        self.dist_threshold = dist_threshold    # Pixel distance threshold for matching

    def register(self, rect, centroid):
        """Registers a newly detected face."""
        self.tracked_faces[self.next_id] = {
            "rect": rect,
            "centroid": centroid,
            "disappeared": 0,
            "last_saved": 0.0,
            "flash_expiry": 0.0
        }
        self.next_id += 1

    def deregister(self, face_id):
        """Deregisters a face that has left the frame."""
        if face_id in self.tracked_faces:
            del self.tracked_faces[face_id]

    def update(self, detected_rects):
        """Updates tracker state by matching detected rectangles to tracked faces."""
        if len(detected_rects) == 0:
            for face_id in list(self.tracked_faces.keys()):
                self.tracked_faces[face_id]["disappeared"] += 1
                if self.tracked_faces[face_id]["disappeared"] > self.max_disappeared:
                    self.deregister(face_id)
            return self.tracked_faces

        detections = []
        for rect in detected_rects:
            x, y, w, h = rect
            cx = x + w // 2
            cy = y + h // 2
            detections.append({"rect": rect, "centroid": (cx, cy)})

        if len(self.tracked_faces) == 0:
            for det in detections:
                self.register(det["rect"], det["centroid"])
            return self.tracked_faces

        face_ids = list(self.tracked_faces.keys())
        tracked_centroids = [self.tracked_faces[fid]["centroid"] for fid in face_ids]

        matched_detections = set()
        matched_faces = set()

        for f_idx, face_id in enumerate(face_ids):
            tcx, tcy = tracked_centroids[f_idx]
            min_dist = float("inf")
            best_det_idx = -1

            for d_idx, det in enumerate(detections):
                if d_idx in matched_detections:
                    continue
                dcx, dcy = det["centroid"]
                dist = math.hypot(dcx - tcx, dcy - tcy)
                if dist < min_dist:
                    min_dist = dist
                    best_det_idx = d_idx

            if best_det_idx != -1 and min_dist < self.dist_threshold:
                det = detections[best_det_idx]
                self.tracked_faces[face_id]["rect"] = det["rect"]
                self.tracked_faces[face_id]["centroid"] = det["centroid"]
                self.tracked_faces[face_id]["disappeared"] = 0
                matched_detections.add(best_det_idx)
                matched_faces.add(face_id)

        for face_id in face_ids:
            if face_id not in matched_faces:
                self.tracked_faces[face_id]["disappeared"] += 1
                if self.tracked_faces[face_id]["disappeared"] > self.max_disappeared:
                    self.deregister(face_id)

        for d_idx, det in enumerate(detections):
            if d_idx not in matched_detections:
                self.register(det["rect"], det["centroid"])

        return self.tracked_faces

# ==========================================
# 5. CUSTOM DRAWING FUNCTIONS (Premium UI)
# ==========================================
def draw_hud_rectangle(img, pt1, pt2, color, thickness=1, corner_len=15, corner_thickness=4):
    """Draws a modern HUD-style bounding box with thick corner brackets."""
    x1, y1 = pt1
    x2, y2 = pt2

    # Draw the main bounding box (thin)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    # Draw the thick corner brackets
    # Top-Left Corner
    cv2.line(img, (x1, y1), (x1 + corner_len, y1), color, corner_thickness)
    cv2.line(img, (x1, y1), (x1, y1 + corner_len), color, corner_thickness)

    # Top-Right Corner
    cv2.line(img, (x2, y1), (x2 - corner_len, y1), color, corner_thickness)
    cv2.line(img, (x2, y1), (x2, y1 + corner_len), color, corner_thickness)

    # Bottom-Left Corner
    cv2.line(img, (x1, y2), (x1 + corner_len, y2), color, corner_thickness)
    cv2.line(img, (x1, y2), (x1, y2 - corner_len), color, corner_thickness)

    # Bottom-Right Corner
    cv2.line(img, (x2, y2), (x2 - corner_len, y2), color, corner_thickness)
    cv2.line(img, (x2, y2), (x2, y2 - corner_len), color, corner_thickness)

# ==========================================
# 6. MAIN APPLICATION ENTRY POINT
# ==========================================
def main():
    download_cascade_if_missing()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize Database table
    init_db()

    face_cascade = cv2.CascadeClassifier(CASCADE_FILENAME)
    if face_cascade.empty():
        print(f"[ERROR] Failed to load cascade classifier from '{CASCADE_FILENAME}'")
        sys.exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        print("[HELP] Make sure your webcam is plugged in and is not being used by another application.")
        sys.exit(1)

    print("[INFO] Camera started.")
    print("       - Press 'C' or 'c' to manually capture all visible faces.")
    print("       - Press 'R' or 'r' to reset the session capture counter.")
    print("       - Press 'Q' or 'q' to exit the application.")

    tracker = FaceTracker(max_disappeared=30, dist_threshold=80)

    # Session stats
    session_captured_count = 0

    # Variables for FPS calculation
    prev_time = time.time()
    fps = 0.0

    # Variables for "Face Captured" Notification Toast
    notification_text = ""
    notification_expiry = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Failed to grab frame from camera.")
            break

        h_frame, w_frame = frame.shape[:2]
        curr_time = time.time()

        # 1. FPS Calculation (Moving Average)
        time_diff = curr_time - prev_time
        prev_time = curr_time
        if time_diff > 0:
            current_fps = 1.0 / time_diff
            fps = (0.9 * fps) + (0.1 * current_fps) if fps > 0.0 else current_fps

        # 2. Convert frame to Grayscale for Haar Cascade detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 3. Detect faces
        face_rects = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # 4. Update the centroid tracker with detected rectangles
        tracked_faces = tracker.update(face_rects)

        # 5. Process tracked faces
        for face_id, face_data in tracked_faces.items():
            x, y, w, h = face_data["rect"]

            # Visual "shutter flash" feedback on bounding box when captured
            if curr_time < face_data.get("flash_expiry", 0.0):
                # Flash Bounding Box (Cyan, thicker, larger corner length)
                box_color = (255, 255, 0)
                corner_len = 22
                corner_thick = 4
            else:
                # Default Bounding Box (Green, clean thickness)
                box_color = (0, 255, 0)
                corner_len = 16
                corner_thick = 3

            # Draw HUD-style rectangle
            draw_hud_rectangle(frame, (x, y), (x + w, y + h), box_color, thickness=1, corner_len=corner_len, corner_thickness=corner_thick)

            # Draw Label with Face ID above box (or below if too high)
            label = f"Face #{face_id}"
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            
            # Position to avoid overlapping the top dashboard bar (75 pixels high)
            label_y = y - 8 if y - 20 > 75 else y + h + text_h + 8
            
            # Draw label block
            cv2.rectangle(frame, (x, label_y - text_h - 4), (x + text_w + 8, label_y + 4), (20, 20, 20), -1)
            cv2.putText(frame, label, (x + 4, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 1, cv2.LINE_AA)

            # Automatic Capture (if cooldown elapsed)
            if curr_time - face_data["last_saved"] >= COOLDOWN_SECONDS:
                # Clamp coordinates to frame boundaries
                x1 = max(0, x)
                y1 = max(0, y)
                x2 = min(w_frame, x + w)
                y2 = min(h_frame, y + h)

                face_crop = frame[y1:y2, x1:x2]

                if face_crop.size > 0:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"face_id{face_id}_{timestamp}.png"
                    filepath = os.path.join(OUTPUT_DIR, filename)

                    # Save crop & Log to Database
                    cv2.imwrite(filepath, face_crop)
                    log_to_db(filename, face_id, "Automatic")

                    # Update face state
                    face_data["last_saved"] = curr_time
                    face_data["flash_expiry"] = curr_time + 0.4  # Trigger flash feedback

                    # Increment session metrics
                    session_captured_count += 1

                    # Trigger visual notification toast
                    notification_text = f"Face #{face_id} Logged!"
                    notification_expiry = curr_time + 1.5

        # ==========================================
        # 6. SEMI-TRANSPARENT DASHBOARD PANEL
        # ==========================================
        # Draw top header panel background (75px tall, 75% opacity)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w_frame, 75), (15, 15, 15), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Dashboard Text - Row 1: Header & Date/Time
        title_text = "SMART ATTENDANCE PORTAL"
        cv2.putText(frame, title_text, (15, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 180, 50), 2, cv2.LINE_AA)

        datetime_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        (dt_w, _), _ = cv2.getTextSize(datetime_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.putText(frame, datetime_text, (w_frame - dt_w - 15, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

        # Dashboard Text - Row 2: Metrics (Organized in horizontal columns)
        # Col 1: FPS (White label, Yellow value)
        fps_lbl = "FPS: "
        fps_val = f"{fps:.1f}"
        (l_w, _), _ = cv2.getTextSize(fps_lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.putText(frame, fps_lbl, (15, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, fps_val, (15 + l_w, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 220, 220), 1, cv2.LINE_AA)

        # Col 2: Active Faces in current frame (White label, Green value)
        faces_lbl = "Active Faces: "
        faces_val = f"{len(face_rects)}"
        (f_w, _), _ = cv2.getTextSize(faces_lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.putText(frame, faces_lbl, (180, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, faces_val, (180 + f_w, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA)

        # Col 3: Session captures (White label, Pink/Magenta value)
        sess_lbl = "Session Saved: "
        sess_val = f"{session_captured_count}"
        (s_w, _), _ = cv2.getTextSize(sess_lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.putText(frame, sess_lbl, (380, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, sess_val, (380 + s_w, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (235, 206, 135), 1, cv2.LINE_AA)

        # ==========================================
        # 7. NOTIFICATION TOAST
        # ==========================================
        if curr_time < notification_expiry:
            (msg_w, msg_h), _ = cv2.getTextSize(notification_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            
            cx_toast = w_frame // 2
            cy_toast = h_frame - 50
            bx1 = cx_toast - msg_w // 2 - 15
            by1 = cy_toast - msg_h // 2 - 8
            bx2 = cx_toast + msg_w // 2 + 15
            by2 = cy_toast + msg_h // 2 + 8

            # Highlight red warning toast if "No faces detected" or "Reset", green otherwise
            toast_color = (0, 0, 150) if "No faces" in notification_text else (0, 120, 0)
            if "Reset" in notification_text:
                toast_color = (150, 75, 0) # Dark Blue/Cyan tint for reset
            
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), toast_color, -1)
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 255, 255), 1)
            cv2.putText(frame, notification_text, (cx_toast - msg_w // 2, cy_toast + msg_h // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

        # bottom status instruction bar
        instr_text = "C: Capture | R: Reset Counter | Q: Exit"
        cv2.putText(frame, instr_text, (15, h_frame - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

        # Display window
        cv2.imshow("Smart Face Detection and Attendance System", frame)

        # Handle Keyboard inputs
        key = cv2.waitKey(1) & 0xFF

        # Exit application
        if key == ord('q') or key == ord('Q'):
            break

        # Reset session count
        elif key == ord('r') or key == ord('R'):
            session_captured_count = 0
            notification_text = "Session Counter Reset!"
            notification_expiry = curr_time + 1.5
            print("[INFO] Session counter has been reset.")

        # Manual face capture trigger
        elif key == ord('c') or key == ord('C'):
            captured_count = 0
            for face_id, face_data in tracked_faces.items():
                # Capture faces that are actively visible in the frame (disappeared == 0)
                if face_data["disappeared"] == 0:
                    x, y, w, h = face_data["rect"]
                    
                    x1 = max(0, x)
                    y1 = max(0, y)
                    x2 = min(w_frame, x + w)
                    y2 = min(h_frame, y + h)
                    
                    face_crop = frame[y1:y2, x1:x2]

                    if face_crop.size > 0:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"face_id{face_id}_manual_{timestamp}.png"
                        filepath = os.path.join(OUTPUT_DIR, filename)

                        cv2.imwrite(filepath, face_crop)
                        log_to_db(filename, face_id, "Manual")

                        # Update face state
                        face_data["last_saved"] = curr_time
                        face_data["flash_expiry"] = curr_time + 0.4

                        captured_count += 1
                        session_captured_count += 1

            if captured_count > 0:
                notification_text = f"Manual Capture! Saved {captured_count} face(s)"
                notification_expiry = curr_time + 2.0
            else:
                notification_text = "No faces detected to capture!"
                notification_expiry = curr_time + 2.0

    print("[INFO] Releasing camera and closing windows...")
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Application closed cleanly.")

if __name__ == "__main__":
    main()
