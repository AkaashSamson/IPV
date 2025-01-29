import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

def main():
    st.title("PIL Image Editor with Streamlit")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Image Processing Options
        option = st.radio("Choose an operation:", 
                          ["Grayscale", "Resize (300x300)", "Rotate (45°)", "Flip Horizontally", "Crop (50,50 to 200,200)", "Draw Box", "Add Text"])
        
        if option == "Grayscale":
            image = image.convert("L")
            st.image(image, caption="Grayscale Image", use_container_width=True)
        
        elif option == "Resize (300x300)":
            image = image.resize((300, 300))
            st.image(image, caption="Resized Image", use_container_width=True)
        
        elif option == "Rotate (45°)":
            image = image.rotate(45)
            st.image(image, caption="Rotated Image", use_container_width=True)
        
        elif option == "Flip Horizontally":
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            st.image(image, caption="Flipped Image", use_container_width=True)
        
        elif option == "Crop (50,50 to 200,200)":
            image = image.crop((50, 50, 200, 200))
            st.image(image, caption="Cropped Image", use_container_width=True)
        
        elif option == "Draw Box":
            draw = ImageDraw.Draw(image)
            draw.rectangle([50, 50, 150, 150], outline="red", width=3)
            st.image(image, caption="Box Drawn Image", use_container_width=True)
        
        elif option == "Add Text":
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            draw.text((50, 50), "Hello, PIL!", fill="white", font=font)
            st.image(image, caption="Text Added", use_container_width=True)
        
        # Download Processed Image
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        st.download_button("Download Processed Image", img_byte_arr.getvalue(), "processed_image.png", "image/png")
        
if __name__ == "__main__":
    main()
