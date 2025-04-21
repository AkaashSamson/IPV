import streamlit as st
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import cv2

# Load DeepLabV3 model (Pretrained on COCO dataset)
model = torch.hub.load("pytorch/vision:v0.10.0", "deeplabv3_resnet101", pretrained=True)
model.eval()

# Image preprocessing function
def preprocess_image(image):
    transform = T.Compose([
        T.Resize((512, 512)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

# Function to get segmentation mask
def get_segmentation_mask(image):
    input_tensor = preprocess_image(image)
    with torch.no_grad():
        output = model(input_tensor)["out"]
    
    mask = output.argmax(1).squeeze().numpy()  # Get predicted labels
    mask = (mask > 0).astype(np.uint8) * 255  # Convert to binary mask (foreground = 255, background = 0)
    return mask

# Streamlit UI
st.title("Image Segmentation with DeepLabV3")

# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Get segmentation mask
    mask = get_segmentation_mask(image)
    
    # Convert mask to displayable format
    mask_display = Image.fromarray(mask)
    
    st.image(mask_display, caption="Segmentation Mask", use_column_width=True)
