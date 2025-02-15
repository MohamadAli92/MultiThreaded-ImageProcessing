import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from Modules.File_handeling import save_image
from Modules.Img_Process import *


def start_process(filter_type):
    try:
        image_path = open_file()
        if not image_path:
            return

        original_image = Image.open(image_path)
        final_img = apply_filter(image_path, filter_type)

        if filter_type == 'bw':
            width = len(final_img[0])
            height = len(final_img)
            processed_image_pil = Image.new('RGB', (width, height))
            for y in range(height):
                for x in range(width):
                    r, g, b = final_img[y][x]
                    processed_image_pil.putpixel((x, y), (r, g, b))
        else:
            width = len(final_img[0])
            height = len(final_img)
            processed_image_pil = Image.new('L', (width, height))
            for y in range(height):
                for x in range(width):
                    gray = final_img[y][x]
                    processed_image_pil.putpixel((x, y), gray)

        original_image_tk = ImageTk.PhotoImage(original_image)
        processed_image_tk = ImageTk.PhotoImage(processed_image_pil)

        # Create a new window for the processed image
        new_window = tk.Toplevel(root)
        new_window.title("Processed Image")

        # Create a frame for the images and labels
        images_frame = ttk.Frame(new_window)
        images_frame.pack(pady=20, padx=20)

        # Original image label
        original_label = ttk.Label(images_frame, text="Original Photo", style="TLabel")
        original_label.grid(row=0, column=0, padx=10, pady=(0, 10))

        # Processed image label
        processed_label = ttk.Label(images_frame, text="Processed Photo", style="TLabel")
        processed_label.grid(row=0, column=1, padx=10, pady=(0, 10))

        # Add labels to display the images
        original_image_label = ttk.Label(images_frame, image=original_image_tk)
        original_image_label.grid(row=1, column=0, padx=10)

        processed_image_label = ttk.Label(images_frame, image=processed_image_tk)
        processed_image_label.grid(row=1, column=1, padx=10)

        # Add the Save Button to the new window
        save_button = tk.Button(new_window, text="Save Image",
                                command=lambda: save_processed_image(processed_image_pil),
                                bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        save_button.pack(pady=20)

        # Store the processed image to be saved
        new_window.image_to_save = processed_image_pil

        # Keep references to the images to prevent garbage collection
        original_image_label.image = original_image_tk
        processed_image_label.image = processed_image_tk

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to open the file dialog for selecting an image
def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".jpg",
                                           filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
    return file_path if file_path else None


# Function to open the file dialog for saving the image
def save_file(image):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"),
                                                            ("BMP files", "*.bmp"), ("TIFF files", "*.tiff")])
        if file_path:
            save_image(image, file_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


# Function to save the processed image
def save_processed_image(processed_image):
    if processed_image:
        save_file(processed_image)
    else:
        messagebox.showwarning("Warning", "No image to save")


# Function to crop the image
def crop_image():
    image_path = open_file()
    if not image_path:
        return

    original_image = Image.open(image_path)
    cropped_image = None  # Initialize as None, to be set after cropping

    # Create a new window for cropping
    crop_window = tk.Toplevel(root)
    crop_window.title("Crop Image")

    canvas = tk.Canvas(crop_window, width=original_image.width, height=original_image.height)
    canvas.pack()

    # Convert the original image to PhotoImage
    original_image_tk = ImageTk.PhotoImage(original_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=original_image_tk)

    # Variables to store cropping rectangle coordinates
    rect_start_x = rect_start_y = rect_end_x = rect_end_y = 0
    rect = None

    def on_button_press(event):
        nonlocal rect_start_x, rect_start_y, rect
        rect_start_x, rect_start_y = event.x, event.y

        # Remove the previous rectangle if it exists
        if rect:
            canvas.delete(rect)

        # Create a new rectangle
        rect = canvas.create_rectangle(rect_start_x, rect_start_y, rect_start_x, rect_start_y, outline="red")

    def on_mouse_drag(event):
        nonlocal rect_end_x, rect_end_y
        rect_end_x, rect_end_y = event.x, event.y
        canvas.coords(rect, rect_start_x, rect_start_y, rect_end_x, rect_end_y)

    def on_button_release(event):
        nonlocal rect_end_x, rect_end_y, rect_start_x, rect_start_y, cropped_image

        rect_end_x, rect_end_y = event.x, event.y

        # Adjust coordinates to ensure (left, top) is always less than (right, bottom)
        if rect_end_x < rect_start_x:
            rect_start_x, rect_end_x = rect_end_x, rect_start_x
        if rect_end_y < rect_start_y:
            rect_start_y, rect_end_y = rect_end_y, rect_start_y

        # Crop only if the selection is valid
        if rect_start_x != rect_end_x and rect_start_y != rect_end_y:
            cropped_image = original_image.crop((rect_start_x, rect_start_y, rect_end_x, rect_end_y))
            # Draw a final rectangle to show the crop area
            canvas.create_rectangle(rect_start_x, rect_start_y, rect_end_x, rect_end_y, outline="red", width=2)

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    # Add the Save Button to the crop window
    save_button = tk.Button(crop_window, text="Save Cropped Image",
                            command=lambda: save_cropped_image(cropped_image),
                            bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
    save_button.pack(pady=20)

    # Keep reference to the image to prevent garbage collection
    crop_window.image = original_image_tk


def save_cropped_image(cropped_image):
    if cropped_image:
        save_file(cropped_image)
    else:
        messagebox.showwarning("Warning", "No cropped image to save")


# Create the main GUI window
root = tk.Tk()
root.title("Image Processing")

# Set the window size
window_width = 600
window_height = 500

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position for the center of the screen
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the style for ttk widgets and apply the "clam" theme
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Helvetica", 14, "bold"), padding=10)
style.configure("TLabel", font=("Helvetica", 16, "bold"), background="#f0f0f0")
style.configure("TFrame", background="#f0f0f0")

# Main frame for organizing widgets
frame = ttk.Frame(root, style="TFrame")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

# Title Label
title_label = ttk.Label(frame, text="Choose one of these effects", style="TLabel")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Filter Buttons
filter_buttons_frame = ttk.Frame(frame, style="TFrame")
filter_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20),
                          sticky=tk.N)  # Add sticky to align the frame to the top

# Create and place filter buttons with different colors (stacked vertically)
sobel_button = ttk.Button(filter_buttons_frame, text="Sobel", command=lambda: start_process('s'), style="TButton")
sobel_button.pack(fill=tk.X, pady=10)

median_button = ttk.Button(filter_buttons_frame, text="Median Blur", command=lambda: start_process('mb'),
                           style="TButton")
median_button.pack(fill=tk.X, pady=10)

blue_and_white_button = ttk.Button(filter_buttons_frame, text="Blue and White", command=lambda: start_process('bw')
                                   , style="TButton")
blue_and_white_button.pack(fill=tk.X, pady=10)

sharpen_button = ttk.Button(filter_buttons_frame, text="Sharpen", command=lambda: start_process('sh'),
                            style="TButton")
sharpen_button.pack(fill=tk.X, pady=10)

# Crop Image Button
crop_button = ttk.Button(filter_buttons_frame, text="Crop Image", command=crop_image, style="TButton")
crop_button.pack(fill=tk.X, pady=10)

# Start the main event loop
root.mainloop()
