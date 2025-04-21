import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class GrayscaleConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grayscale Image Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.current_image_path = None
        self.original_image = None
        self.preview_image = None
        self.selected_method = tk.StringVar(value="Luminosity (BT.709)")

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel for controls
        left_panel = ttk.Frame(main_frame, padding=10, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        # Title
        title_label = ttk.Label(
            left_panel, text="Grayscale Converter", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Method selection
        method_label = ttk.Label(left_panel, text="Select Conversion Method:")
        method_label.pack(anchor=tk.W, pady=(0, 5))

        methods = [
            "Averaging",
            "Luminosity (BT.709)",
            "Lightness",
            "Single Channel",
            "Desaturation",
            "Luma (BT.601)",
        ]

        for method in methods:
            rb = ttk.Radiobutton(
                left_panel,
                text=method,
                value=method,
                variable=self.selected_method,
                command=self.update_preview,
            )
            rb.pack(anchor=tk.W, pady=2)

        # Buttons
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill=tk.X, pady=10)

        select_btn = ttk.Button(
            button_frame, text="Select Image", command=self.select_image
        )
        select_btn.pack(fill=tk.X, pady=5)

        convert_btn = ttk.Button(
            button_frame, text="Convert Image", command=self.convert_image
        )
        convert_btn.pack(fill=tk.X, pady=5)

        # Right panel for image preview
        self.right_panel = ttk.Frame(main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Image preview
        self.preview_label = ttk.Label(self.right_panel, text="No image selected")
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
        )

        if not file_path:
            return

        self.current_image_path = file_path
        self.original_image = Image.open(file_path)
        self.update_preview()
        self.status_var.set(f"Image loaded: {os.path.basename(file_path)}")

    def update_preview(self):
        if not self.original_image:
            return

        # Convert image based on selected method for preview
        if self.selected_method.get() == "Single Channel":
            # For preview, just show green channel
            grayscale_image = self.convert_to_grayscale(
                self.original_image, "Single Channel (Green)"
            )
        else:
            grayscale_image = self.convert_to_grayscale(
                self.original_image, self.selected_method.get()
            )

        # Resize for preview if needed
        max_width = self.right_panel.winfo_width() - 20
        max_height = self.right_panel.winfo_height() - 20

        if max_width > 0 and max_height > 0:
            # Calculate scaling factor to fit the image in the panel
            img_width, img_height = grayscale_image.size
            scale = min(max_width / img_width, max_height / img_height)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            if scale < 1:
                preview_img = grayscale_image.resize(
                    (new_width, new_height), Image.LANCZOS
                )
            else:
                preview_img = grayscale_image

            self.preview_image = ImageTk.PhotoImage(preview_img)
            self.preview_label.config(image=self.preview_image, text="")
        else:
            # Handle the case when the panel isn't fully realized yet
            self.root.after(100, self.update_preview)

    def convert_to_grayscale(self, image, method):
        # Create a copy to avoid modifying the original
        img = image.convert("RGB")
        width, height = img.size

        if method == "Averaging":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))
                    gray_value = int((r + g + b) / 3)
                    grayscale_image.putpixel((x, y), gray_value)

        elif method == "Luminosity (BT.709)":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))
                    gray_value = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                    grayscale_image.putpixel((x, y), gray_value)

        elif method == "Lightness" or method == "Desaturation":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))
                    gray_value = int((max(r, g, b) + min(r, g, b)) / 2)
                    grayscale_image.putpixel((x, y), gray_value)

        elif method == "Single Channel (Red)":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    r, _, _ = img.getpixel((x, y))
                    grayscale_image.putpixel((x, y), r)

        elif method == "Single Channel (Green)":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    _, g, _ = img.getpixel((x, y))
                    grayscale_image.putpixel((x, y), g)

        elif method == "Single Channel (Blue)":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    _, _, b = img.getpixel((x, y))
                    grayscale_image.putpixel((x, y), b)

        elif method == "Luma (BT.601)":
            grayscale_image = Image.new("L", (width, height))
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))
                    gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                    grayscale_image.putpixel((x, y), gray_value)

        return grayscale_image

    def convert_image(self):
        if not self.original_image:
            self.status_var.set("Please select an image first")
            return

        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), "grayscale_images")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get base filename
        filename = os.path.basename(self.current_image_path)
        name, ext = os.path.splitext(filename)
        method = self.selected_method.get()

        # Process based on selected method
        if method == "Single Channel":
            # Process each channel separately
            for channel in ["Red", "Green", "Blue"]:
                grayscale_image = self.convert_to_grayscale(
                    self.original_image, f"Single Channel ({channel})"
                )

                # Create method-specific filename
                output_path = os.path.join(
                    output_dir, f"{name}_SingleChannel_{channel}{ext}"
                )

                # Save the image
                grayscale_image.save(output_path)

            self.status_var.set(f"Single Channel images saved to {output_dir}")
        else:
            # Process using the selected method
            grayscale_image = self.convert_to_grayscale(self.original_image, method)

            # Create method-specific filename (replace spaces and special chars)
            method_name = (
                method.replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace(".", "")
            )
            output_path = os.path.join(output_dir, f"{name}_{method_name}{ext}")

            # Save the image
            grayscale_image.save(output_path)

            self.status_var.set(f"Image saved as {os.path.basename(output_path)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GrayscaleConverterApp(root)

    # Update preview when window is resized
    def on_resize(event):
        if hasattr(app, "original_image") and app.original_image:
            # Use after to avoid multiple calls during resize
            root.after_cancel(app.resize_job) if hasattr(app, "resize_job") else None
            app.resize_job = root.after(100, app.update_preview)

    app.right_panel.bind("<Configure>", on_resize)
    root.mainloop()
