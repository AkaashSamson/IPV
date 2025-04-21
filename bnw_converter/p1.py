import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def convert_to_grayscale(image):
    # Create a new image the same size as the original
    width, height = image.size
    grayscale_image = Image.new("L", (width, height))

    # Process each pixel
    for x in range(width):
        for y in range(height):
            # Get RGB values of the pixel
            r, g, b = image.getpixel((x, y))[:3]

            # Calculate grayscale value using luminosity method
            # The formula 0.299R + 0.587G + 0.114B is a common
            # weighting to account for human perception
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Set the grayscale pixel
            grayscale_image.putpixel((x, y), gray_value)

    return grayscale_image


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

    # Open the selected image
    try:
        original_image = Image.open(file_path)

        # Convert to black and white using our custom function
        bw_image = convert_to_grayscale(original_image)

        # Create the output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "black and white")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get the original filename and prepare the output path
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_bw{ext}")

        # Save the black and white image
        bw_image.save(output_path)
        print(f"Black and white image saved to: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    select_image()
