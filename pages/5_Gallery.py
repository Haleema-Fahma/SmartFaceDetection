import streamlit as st
import os
from PIL import Image

st.title("🖼 Captured Faces")

folder = "CapturedFaces"

if os.path.exists(folder):

    images = os.listdir(folder)

    if len(images)==0:
        st.info("No captured faces.")

    cols = st.columns(3)

    for i,img in enumerate(images):

        path = os.path.join(folder,img)

        cols[i%3].image(
            Image.open(path),
            caption=img
        )

else:

    st.warning("CapturedFaces folder not found.")