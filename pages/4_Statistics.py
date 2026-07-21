import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Statistics")

try:

    conn = sqlite3.connect("attendance.db")

    df = pd.read_sql_query(
        "SELECT * FROM attendance",
        conn
    )

    conn.close()

    total = len(df)

    st.metric(
        "Total Attendance Records",
        total
    )

    st.metric(
        "Unique Face IDs",
        df["face_id"].nunique()
    )

except:

    st.info("Database is empty.")