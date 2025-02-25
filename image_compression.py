import tkinter as tk  
from tkinter import filedialog, messagebox  
from PIL import Image, ImageTk  
import os  

# Compress image to JPEG format
def compress_to_jpeg(input_path, output_path, quality):
    try:
        image = Image.open(input_path)
        image.save(output_path, "JPEG", quality=quality, optimize=True)
        return os.path.getsize(output_path) / 1024  # Return size in KB
    except Exception as e:
        messagebox.showerror("Error", f"Error compressing to JPEG: {e}")
        return None  

# Compress image to PNG format
def compress_to_png(input_path, output_path, compression_level):
    try:
        image = Image.open(input_path)
        image.save(output_path, "PNG", optimize=True, compress_level=compression_level)
        return os.path.getsize(output_path) / 1024  
    except Exception as e:
        messagebox.showerror("Error", f"Error compressing to PNG: {e}")
        return None  

# Handle compression selection
def select_compression_type():
    compression_type = compression_choice.get()
    if compression_type == "JPEG":
        compress_jpeg()
    elif compression_type == "PNG":
        compress_png()

# JPEG compression process
def compress_jpeg():
    input_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg")])
    if not input_image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
    if not output_path:
        messagebox.showerror("Error", "File Name not provided.")
        return

    try:
        jpeg_quality = int(quality_var.get())
        jpeg_size = compress_to_jpeg(input_image_path, output_path, jpeg_quality)
        if jpeg_size:
            display_results(input_image_path, output_path, jpeg_size)
    except Exception as e:
        messagebox.showerror("Error", f"Error during compression: {e}")

# PNG compression process
def compress_png():
    input_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if not input_image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if not output_path:
        messagebox.showerror("Error", "File Name not provided.")
        return

    try:
        png_compression_level = int(png_quality_var.get())
        png_size = compress_to_png(input_image_path, output_path, png_compression_level)
        if png_size:
            display_results(input_image_path, output_path, png_size)
    except Exception as e:
        messagebox.showerror("Error", f"Error during compression: {e}")

# Display results after compression
def display_results(original_path, compressed_path, compressed_size):
    try:
        original_size = os.path.getsize(original_path) / 1024  
        display_image(original_path, original_label)
        display_image(compressed_path, compressed_label)
        results_text.set(f"Original Size: {original_size:.2f} KB\nCompressed Size: {compressed_size:.2f} KB")
    except Exception as e:
        messagebox.showerror("Error", f"Error displaying results: {e}")

# Display image in the UI
def display_image(image_path, label):
    try:
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img  
    except Exception as e:
        messagebox.showerror("Error", f"Error displaying image: {e}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Image Compression Tool")
root.geometry("600x760")
root.configure(bg="#ffffff")

# Create scrollable UI
canvas = tk.Canvas(root, bg="#ffffff")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#ffffff")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# UI Elements
instruction_label = tk.Label(scrollable_frame, text="Select Compression Type (JPEG or PNG)", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#888")
instruction_label.pack(pady=20)

compression_choice = tk.StringVar(value="JPEG")
jpeg_button = tk.Radiobutton(scrollable_frame, text="JPEG", variable=compression_choice, value="JPEG", font=("Arial", 14), bg="#f0f0f0", fg="#333")
jpeg_button.pack(pady=5)

png_button = tk.Radiobutton(scrollable_frame, text="PNG", variable=compression_choice, value="PNG", font=("Arial", 14), bg="#f0f0f0", fg="#333")
png_button.pack(pady=5)

quality_label = tk.Label(scrollable_frame, text="JPEG Quality (1-100):", font=("Arial", 12), bg="#f0f0f0", fg="#333")
quality_label.pack(pady=10)

quality_var = tk.StringVar(value="50")
quality_entry = tk.Entry(scrollable_frame, textvariable=quality_var, width=12, font=("Arial", 12), bg="#ffffff", fg="#333")
quality_entry.pack(pady=5)

png_quality_label = tk.Label(scrollable_frame, text="PNG Compression Level (0-9):", font=("Arial", 12), bg="#f0f0f0", fg="#333")
png_quality_label.pack(pady=10)

png_quality_var = tk.StringVar(value="5")
png_quality_entry = tk.Entry(scrollable_frame, textvariable=png_quality_var, width=12, font=("Arial", 12), bg="#ffffff", fg="#333")
png_quality_entry.pack(pady=5)

select_button = tk.Button(scrollable_frame, text="Select Compression", command=select_compression_type, width=25, font=("Arial", 14), bg="#4CAF50", fg="white")
select_button.pack(pady=20)

original_label = tk.Label(scrollable_frame, text="Original Image Preview", font=("Arial", 12), bg="#f0f0f0", fg="#333")
original_label.pack(pady=5)
original_label = tk.Label(scrollable_frame, bg="#f0f0f0")
original_label.pack()

compressed_label = tk.Label(scrollable_frame, text="Compressed Image Preview", font=("Arial", 12), bg="#f0f0f0", fg="#333")
compressed_label.pack(pady=5)
compressed_label = tk.Label(scrollable_frame, bg="#f0f0f0")
compressed_label.pack()

results_text = tk.StringVar()
results_label = tk.Label(scrollable_frame, textvariable=results_text, font=("Arial", 14), bg="#f0f0f0", fg="#333", justify="left")
results_label.pack(pady=20)

footer_label = tk.Label(scrollable_frame, text="Image Compression Tool | Made By Ahsan Ahmed", font=("Arial", 10), bg="#333", fg="white")
footer_label.pack(side="bottom", fill="x", pady=10)

# Run Tkinter application
root.mainloop()
