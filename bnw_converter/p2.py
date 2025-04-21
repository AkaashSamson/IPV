import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import cv2


def select_image():
    # Open file dialog to select an image
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
    )

    if not file_path:
        print("No image selected")
        return

    # Process the image
    try:
        # Original black and white conversion
        original_image = Image.open(file_path)
        bw_image = original_image.convert("L")

        # Create output directories if they don't exist
        bw_dir = os.path.join(os.path.dirname(__file__), "black and white")
        mono_dir = os.path.join(os.path.dirname(__file__), "monochrome")

        for directory in [bw_dir, mono_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Get the original filename and prepare the output paths
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        bw_path = os.path.join(bw_dir, f"{name}_bw{ext}")
        mono_path = os.path.join(mono_dir, f"{name}_mono{ext}")

        # Save the black and white image
        bw_image.save(bw_path)
        print(f"Black and white image saved to: {bw_path}")

        # Create monochrome image (color foreground, B&W background)
        # Convert PIL Image to OpenCV format
        cv_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)

        # Create a mask using image segmentation
        # Using GrabCut for foreground extraction
        mask = np.zeros(cv_image.shape[:2], np.uint8)
        rect = (
            10,
            10,
            cv_image.shape[1] - 20,
            cv_image.shape[0] - 20,
        )  # Initial rectangle

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Apply GrabCut
        cv2.grabCut(cv_image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # Create a mask where probable and definite foreground are set to 1
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

        # Convert image to grayscale for background
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

        # Create monochrome image: foreground in color, background in grayscale
        for i in range(3):  # Apply for each color channel
            gray_image[:, :, i] = (
                gray_image[:, :, i] * (1 - mask2) + cv_image[:, :, i] * mask2
            )

        # Convert back to PIL and save
        monochrome_image = Image.fromarray(cv2.cvtColor(gray_image, cv2.COLOR_BGR2RGB))
        monochrome_image.save(mono_path)
        print(f"Monochrome image saved to: {mono_path}")

    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    select_image()
