import streamlit as st
import cv2
import numpy as np
from PIL import Image
import sqlite3
from datetime import datetime
import os
from pathlib import Path

st.set_page_config(page_title="Face Detection", page_icon="📷")

st.title("📷 Face Detection")

# -----------------------------
# Load Haar Cascade safely
# -----------------------------
cascade_path = Path(__file__).parent.parent / "haarcascade_frontalface_default.xml"

if not cascade_path.exists():
    st.error(f"Haar Cascade file not found:\n{cascade_path}")
    st.stop()

cascade = cv2.CascadeClassifier(str(cascade_path))

if cascade.empty():
    st.error("Failed to load Haar Cascade classifier.")
    st.stop()

# -----------------------------
# Create required folders/files
# -----------------------------
os.makedirs("CapturedFaces", exist_ok=True)

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    face_id INTEGER,
    image_filename TEXT,
    capture_type TEXT
)
""")

conn.commit()
conn.close()

# -----------------------------
# Upload image
# -----------------------------
uploaded = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:

    image = Image.open(uploaded).convert("RGB")
    image = np.array(image)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    st.success(f"Faces Detected: {len(faces)}")

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    for i, (x, y, w, h) in enumerate(faces):

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        face = image[y:y+h, x:x+w]

        filename = f"face_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"

        filepath = os.path.join("CapturedFaces", filename)

        cv2.imwrite(
            filepath,
            cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
        )

        now = datetime.now()

        cur.execute("""
        INSERT INTO attendance(
            date,
            time,
            face_id,
            image_filename,
            capture_type
        )
        VALUES(?,?,?,?,?)
        """,
        (
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            i + 1,
            filename,
            "Image Upload"
        ))

    conn.commit()
    conn.close()

    st.image(image, caption="Detected Faces", use_container_width=True)

    st.success("Attendance saved successfully!")