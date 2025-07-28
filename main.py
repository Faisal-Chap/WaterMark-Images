import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# --- Function to Open Image ---
def open_image():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize to fit in window
            tk_img = ImageTk.PhotoImage(img)
            image_label.config(image=tk_img)
            image_label.image = tk_img
            app.image = img
            status_label.config(text=f"Loaded: {file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Invalid File", "The selected file is not a valid image.")

# --- Function to Add Watermark ---
def add_watermark():
    if hasattr(app, 'image'):
        img = app.image.copy()
        draw = ImageDraw.Draw(img)
        text = "Watermark"
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        draw.text((10, 10), text, font=font, fill=(255, 255, 255, 128))
        img.thumbnail((400, 400))  # Resize preview
        tk_img = ImageTk.PhotoImage(img)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        app.watermarked = img
        status_label.config(text="✅ Watermark added")

# --- Function to Save Watermarked Image ---
def save_image():
    if hasattr(app, 'watermarked'):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")])
        if file_path:
            try:
                app.watermarked.save(file_path)
                status_label.config(text=f"💾 Saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", "Could not save the image.")

# --- GUI Setup ---
app = tk.Tk()
app.title("🖼️ Image Watermarker")
app.geometry("600x500")
app.minsize(500, 450)

# --- Buttons ---
open_button = tk.Button(app, text="📂 Open Image", command=open_image, width=20)
open_button.pack(pady=10)

watermark_button = tk.Button(app, text="💧 Add Watermark", command=add_watermark, width=20)
watermark_button.pack(pady=5)

save_button = tk.Button(app, text="💾 Save Image", command=save_image, width=20)
save_button.pack(pady=5)

# --- Image Display ---
image_label = tk.Label(app)
image_label.pack(pady=10)

# --- Status Message ---
status_label = tk.Label(app, text="Select an image to begin.", fg="gray")
status_label.pack(pady=5)

# --- Mainloop ---
app.mainloop()
