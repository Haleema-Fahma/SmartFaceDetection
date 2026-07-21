import streamlit as st
import sqlite3
import pandas as pd

st.title("📋 Attendance Records")

try:
    conn = sqlite3.connect("attendance.db")

    df = pd.read_sql_query(
        "SELECT * FROM attendance",
        conn
    )

    conn.close()

    st.dataframe(df, use_container_width=True)

except Exception:
    st.warning("No attendance records found.")