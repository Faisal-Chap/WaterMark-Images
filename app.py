import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import colorchooser




class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Image Watermarker")
        self.root.geometry("900x850")
        self.root.minsize(800, 600)  # Sets a reasonable minimum size


        # --- Canvas for Image Preview ---
        self.image_canvas = tk.Canvas(root, bg="#f0f0f0", width=800, height=550)
        self.image_canvas.pack(pady=10)

        self.image_on_canvas = None
        self.image_path = None
        self.pil_image = None

        # Default text color for watermark
        self.text_color = (255, 255, 255)  # default white






        # --- Zoom and Move Support ---
        self.zoom_level = 1.0
        self.image_offset = [0, 0]
        self.drag_start = None

        # --- Placeholder Text ---
        self.text_overlay = self.image_canvas.create_text(
            400, 275, text="No image selected", fill="gray",
            font=("Helvetica", 18), justify="center"
        )

        # --- Buttons ---
        button_frame = tk.Frame(root)
        button_frame.pack()

        import_btn = tk.Button(button_frame, text="📂 Import Image", command=self.open_image)
        import_btn.grid(row=0, column=0, padx=10)

        zoom_in_btn = tk.Button(button_frame, text="➕ Zoom In", command=self.zoom_in)
        zoom_in_btn.grid(row=0, column=1, padx=10)

        zoom_out_btn = tk.Button(button_frame, text="➖ Zoom Out", command=self.zoom_out)
        zoom_out_btn.grid(row=0, column=2, padx=10)

        # --- Mouse Events for Moving Image ---
        self.image_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.image_canvas.bind("<B1-Motion>", self.do_drag)

    # -------- Image Loading --------
    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.pil_image = Image.open(file_path)
            self.zoom_level = 1.0
            self.image_offset = [0, 0]
            self.update_canvas_image()
        self.build_controls()


    # -------- Zoom Buttons --------
    def zoom_in(self):
        self.zoom_level *= 1.1
        self.update_canvas_image()

    def zoom_out(self):
        self.zoom_level /= 1.1
        self.update_canvas_image()

    # -------- Drag Events --------
    def start_drag(self, event):
        self.drag_start = (event.x, event.y)

    def do_drag(self, event):
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.image_offset[0] += dx
            self.image_offset[1] += dy
            self.drag_start = (event.x, event.y)
            self.update_canvas_image()

    # -------- Render Updated Image on Canvas --------
    def update_canvas_image(self):
        if self.pil_image:
            w, h = self.pil_image.size
            zoomed = self.pil_image.resize(
                (int(w * self.zoom_level), int(h * self.zoom_level)),
                Image.LANCZOS
            )
            tk_image = ImageTk.PhotoImage(zoomed)

            # Clear previous image or text
            if self.image_on_canvas:
                self.image_canvas.delete(self.image_on_canvas)
            self.image_canvas.delete(self.text_overlay)

            cx = 400 + self.image_offset[0]
            cy = 225 + self.image_offset[1]
            self.image_on_canvas = self.image_canvas.create_image(cx, cy, image=tk_image)
            self.image_canvas.image = tk_image  # Prevent garbage collection
    

    # watermark build controls 
    def build_controls(self):
        # Only create once
        if hasattr(self, 'control_frame'):
            return

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # --- Watermark Text Entry ---
        tk.Label(self.control_frame, text="Watermark Text:").grid(row=0, column=0)
        self.text_entry = tk.Entry(self.control_frame, width=30)
        self.text_entry.grid(row=0, column=1, padx=10)
        self.text_entry.insert(0, "Sample Watermark")

        # --- Font Size Slider ---
        tk.Label(self.control_frame, text="Font Size:").grid(row=1, column=0)
        self.font_size_slider = tk.Scale(self.control_frame, from_=10, to=100, orient='horizontal')
        self.font_size_slider.set(32)
        self.font_size_slider.grid(row=1, column=1, sticky='ew', padx=10)

        # --- Opacity Slider ---
        tk.Label(self.control_frame, text="Opacity (%):").grid(row=2, column=0)
        self.opacity_slider = tk.Scale(self.control_frame, from_=10, to=100, orient='horizontal')
        self.opacity_slider.set(80)
        self.opacity_slider.grid(row=2, column=1, sticky='ew', padx=10)

        # --- Rotation Slider ---
        tk.Label(self.control_frame, text="Rotation (°):").grid(row=3, column=0)
        self.rotation_slider = tk.Scale(self.control_frame, from_=0, to=360, orient='horizontal')
        self.rotation_slider.set(0)
        self.rotation_slider.grid(row=3, column=1, sticky='ew', padx=10)

        # --- Action Buttons ---
        # --- Color Selection Button and Preview ---
        color_button = tk.Button(self.control_frame, text="Pick Text Color", command=self.choose_text_color)
        color_button.grid(row=4, column=0, pady=10)
        
        # Color preview label - NOW created after control_frame exists
        self.color_preview = tk.Label(self.control_frame, width=2, background="#FFFFFF")
        self.color_preview.grid(row=4, column=1, padx=5)

        # --- Action Buttons ---
        apply_btn = tk.Button(self.control_frame, text="💧 Apply Watermark", command=self.apply_watermark)
        apply_btn.grid(row=5, column=0, pady=10)

        save_btn = tk.Button(self.control_frame, text="💾 Save Image", command=self.save_image)
        save_btn.grid(row=5, column=1, pady=10)
        # Bind events to update watermark preview
        self.text_entry.bind("<KeyRelease>", lambda e: self.apply_watermark())
        self.font_size_slider.config(command=lambda x: self.apply_watermark())
        self.opacity_slider.config(command=lambda x: self.apply_watermark())
        self.rotation_slider.config(command=lambda x: self.apply_watermark())



    # -------- Choose Text Color --------

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[0]:
            self.text_color = tuple(map(int, color[0]))
            hex_color = color[1]
            self.color_preview.config(background=hex_color)
            self.apply_watermark()



    # -------- Apply Watermark --------
    def apply_watermark(self):
        if not self.pil_image:
            return

        base = self.pil_image.convert("RGBA")
        text = self.text_entry.get()
        font_size = self.font_size_slider.get()
        opacity = self.opacity_slider.get()
        rotation = self.rotation_slider.get()

        try:
            font = ImageFont.truetype("DejaVuSans.ttf", int(font_size))
        except OSError:
            print("Font not found. Falling back to default (may be small).")
            font = ImageFont.load_default()


        # Create watermark text image
        # Step 1: Calculate text size
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Step 2: Create transparent image just for text
        text_img = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_img)
        fill = (*self.text_color, int(255 * opacity / 100))
        draw.text((0, 0), text, font=font, fill=fill)
        # Step 3: Rotate the watermark
        rotated_text = text_img.rotate(rotation, expand=1)

        # Step 4: Create overlay same size as base
        overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
        x = (base.width - rotated_text.width) // 2
        y = (base.height - rotated_text.height) // 2
        overlay.paste(rotated_text, (x, y), rotated_text)

        # Step 5: Composite
        watermarked = Image.alpha_composite(base, overlay)

        self.watermarked_image = watermarked.convert("RGB")
        self.show_watermarked_preview()


    # -------- Show Watermarked Preview --------
    def show_watermarked_preview(self):
        # Show result on canvas
        preview = self.watermarked_image.copy()
        w, h = preview.size
        preview = preview.resize(
            (int(w * self.zoom_level), int(h * self.zoom_level)),
            Image.LANCZOS
        )
        tk_image = ImageTk.PhotoImage(preview)

        if self.image_on_canvas:
            self.image_canvas.delete(self.image_on_canvas)

        cx = 400 + self.image_offset[0]
        cy = 225 + self.image_offset[1]
        self.image_on_canvas = self.image_canvas.create_image(cx, cy, image=tk_image)
        self.image_canvas.image = tk_image




    # -------- Save Watermarked Image --------

    def save_image(self):
        if hasattr(self, 'watermarked_image'):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
            )
            if file_path:
                self.watermarked_image.save(file_path)


# -------- Launch App --------
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
