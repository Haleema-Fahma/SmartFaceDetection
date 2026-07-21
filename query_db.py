"""
Smart Face Detection and Attendance System - Query Helper
==========================================================
A simple utility script to connect to attendance.db and display
logged records in a neat tabular layout in the console.

Author: Senior Python & OpenCV Developer
"""

import sqlite3
import os

DB_FILENAME = "attendance.db"

def query_attendance():
    if not os.path.exists(DB_FILENAME):
        print(f"[ERROR] Database file '{DB_FILENAME}' does not exist yet.")
        print("Please run 'python app.py' first to start logging attendance.")
        return

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        
        # Select all records ordered by ID
        cursor.execute("SELECT id, date, time, face_id, image_filename, capture_type FROM attendance ORDER BY id ASC")
        records = cursor.fetchall()
        
        if len(records) == 0:
            print("[INFO] Attendance database is initialized but contains no logs yet.")
            conn.close()
            return
            
        print("\n" + "=" * 90)
        print(f"{'ID':<5} | {'Date':<12} | {'Time':<10} | {'Face ID':<8} | {'Filename':<35} | {'Type':<10}")
        print("=" * 90)
        
        for row in records:
            print(f"{row[0]:<5} | {row[1]:<12} | {row[2]:<10} | {row[3]:<8} | {row[4]:<35} | {row[5]:<10}")
            
        print("=" * 90)
        print(f"Total Logged Records: {len(records)}\n")
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Failed to query database: {e}")

if __name__ == "__main__":
    query_attendance()
