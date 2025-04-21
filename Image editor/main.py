import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Image Editor using Streamlit and OpenCV")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Convert the image to OpenCV format
    image_cv = np.array(image.convert('RGB'))
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

    # Example operation: Convert to grayscale
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Display the processed image
    st.image(gray_image, caption='Processed Image (Grayscale)', use_column_width=True)