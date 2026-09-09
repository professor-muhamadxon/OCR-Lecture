import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw
import image as i
import os

class ImageOptimizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image Optimizer')
        self.geometry('1000x800')
        self.image_path = None
        self.optimized_image_path = None
        self.pan_offset = [0, 0]
        self.bbox_rect = None
        self.config(bg="black") 
        # Main horizontal layout
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        main_frame.config(bg="black")

        # Left: Image display
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        left_frame.config(bg="black")
        self.canvas = tk.Canvas(left_frame, bg='#f0f0f0', width=400, height=400, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=5, pady=5)
        self.canvas_img = None
        self.canvas.bind('<ButtonPress-1>', self.start_pan)
        self.canvas.bind('<B1-Motion>', self.do_pan)
        self.canvas.config(bg="black")

        # Zoom controls
        zoom_frame = tk.Frame(left_frame)
        zoom_frame.pack(pady=5)
        tk.Button(zoom_frame, text='Zoom In', command=self.zoom_in).pack(side='left', padx=5)
        tk.Button(zoom_frame, text='Zoom Out', command=self.zoom_out).pack(side='left', padx=5)
        tk.Button(zoom_frame, text='Restore', command=self.restore_image).pack(side='left', padx=5)

        # Right: Optimizer params
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='y', padx=10)
        right_frame.config(bg="black")

        # BBOX koordinatalari uchun Entry maydonlari
        bbox_frame = tk.Frame(right_frame)
        bbox_frame.pack(pady=1, fill='x')
        bbox_frame.config(bg="black")
        tk.Label(bbox_frame, text='x1').pack(side='left')
        self.bbox_x1 = tk.IntVar(value=240)
        tk.Entry(bbox_frame, textvariable=self.bbox_x1, width=5).pack(side='left')
        tk.Label(bbox_frame, text='y1').pack(side='left')
        self.bbox_y1 = tk.IntVar(value=200)
        tk.Entry(bbox_frame, textvariable=self.bbox_y1, width=5).pack(side='left')
        tk.Label(bbox_frame, text='x2').pack(side='left')
        self.bbox_x2 = tk.IntVar(value=1900)
        tk.Entry(bbox_frame, textvariable=self.bbox_x2, width=5).pack(side='left')
        tk.Label(bbox_frame, text='y2').pack(side='left')
        self.bbox_y2 = tk.IntVar(value=2710)
        tk.Entry(bbox_frame, textvariable=self.bbox_y2, width=5).pack(side='left')

        self.bbox_label = tk.Label(right_frame, text='BBOX: N/A')
        self.bbox_label.pack(pady=1, fill='x')
        self.draw_btn = tk.Button(right_frame, text='Draw', command=self.draw_bbox_rect)
        self.draw_btn.pack(pady=1, fill='x')
        self.flip_btn = tk.Button(right_frame, text='Flip', command=self.flip_image)
        self.flip_btn.pack(pady=1, fill='x')
        self.clip_btn = tk.Button(right_frame, text='Clip', command=self.clip_image)
        self.clip_btn.pack(pady=1, fill='x')
        self.load_btn = tk.Button(right_frame, text='Load Image', command=self.load_image)
        self.load_btn.pack(pady=1, fill='x')
        self.image_mode_label = tk.Label(right_frame, text='Image Mode: N/A')
        self.image_mode_label.pack(pady=(0, 1), fill='x')

        # Colorizer params
        colorizer_label = tk.Label(right_frame, text='Colorizer RGB Factors (0-2)')
        colorizer_label.pack(pady=(1, 0))
        colorizer_frame = tk.Frame(right_frame)
        colorizer_frame.pack(pady=1)
        self.colorizer_r = tk.DoubleVar(value=1.1)
        self.colorizer_g = tk.DoubleVar(value=1.1)
        self.colorizer_b = tk.DoubleVar(value=1.1)
        tk.Entry(colorizer_frame, textvariable=self.colorizer_r, width=4).pack(side='left', padx=2)
        tk.Entry(colorizer_frame, textvariable=self.colorizer_g, width=4).pack(side='left', padx=2)
        tk.Entry(colorizer_frame, textvariable=self.colorizer_b, width=4).pack(side='left', padx=2)

        # Luminancer params
        luminancer_label = tk.Label(right_frame, text='Luminancer RGB Weights (0-1, sum~1)')
        luminancer_label.pack(pady=(1, 0))
        luminancer_frame = tk.Frame(right_frame)
        luminancer_frame.pack(pady=1)
        self.luminancer_r = tk.DoubleVar(value=0.33)
        self.luminancer_g = tk.DoubleVar(value=0.33)
        self.luminancer_b = tk.DoubleVar(value=0.34)
        tk.Entry(luminancer_frame, textvariable=self.luminancer_r, width=4).pack(side='left', padx=2)
        tk.Entry(luminancer_frame, textvariable=self.luminancer_g, width=4).pack(side='left', padx=2)
        tk.Entry(luminancer_frame, textvariable=self.luminancer_b, width=4).pack(side='left', padx=2)

        # Binarization threshold
        self.slider_label = tk.Label(right_frame, text='Binarization Threshold (%)')
        self.slider_label.pack(pady=(1, 0))
        self.threshold = tk.IntVar(value=80)
        self.slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.threshold, length=180)
        self.slider.pack(pady=1)

        # Extrude param
        extrude_label = tk.Label(right_frame, text='Extrude Pixel (1-10)')
        extrude_label.pack(pady=(1, 0))
        extrude_frame = tk.Frame(right_frame)
        extrude_frame.pack(pady=1)
        self.extrude_pixel = tk.IntVar(value=3)
        tk.Entry(extrude_frame, textvariable=self.extrude_pixel, width=4).pack(pady=1)
        self.extrude_pixel_w = tk.IntVar(value=5)
        tk.Entry(extrude_frame, textvariable=self.extrude_pixel_w, width=4).pack(pady=1)

        # MinMaxHeight param
        minmax_label = tk.Label(right_frame, text='Min Max Height(1-100)')
        minmax_label.pack(pady=(1, 0))
        minmax_frame = tk.Frame(right_frame)
        minmax_frame.pack(pady=1)
        self.min_height = tk.IntVar(value=10)
        self.max_height = tk.IntVar(value=120)
        self.max_width = tk.IntVar(value=600)
        tk.Entry(minmax_frame, textvariable=self.min_height, width=4).pack(side="left", padx=2)
        tk.Entry(minmax_frame, textvariable=self.max_height, width=4).pack(side="left", padx=2)
        tk.Entry(minmax_frame, textvariable=self.max_width, width=4).pack(side="left", padx=2)

        self.optimize_btn = tk.Button(right_frame, text='Optimize', command=self.optimize_image)
        self.optimize_btn.pack(pady=1, fill='x')
        self.extrude_btn = tk.Button(right_frame, text='Extrude', command=self.extrude_image)
        self.extrude_btn.pack(pady=1, fill='x')
        self.save_btn = tk.Button(right_frame, text='Save', command=self.save_image)
        self.save_btn.pack(pady=1, fill='x')
        self.segment_btn = tk.Button(right_frame, text='Segmentation', command=self.segment_image)
        self.segment_btn.pack(pady=1, fill='x')
        self.to1_btn = tk.Button(right_frame, text="Convert to '1' mode", command=self.convert_to_1_mode)
        self.to1_btn.pack(pady=1, fill='x')
        self.segment_diagram_btn = tk.Button(right_frame, text='Segmentation Diagram', command=self.show_segmentation_diagram)
        self.segment_diagram_btn.pack(pady=1, fill='x')
        self.filter_btn = tk.Button(right_frame, text='Filter Segmentation', command=self.filter_segmentation)
        self.filter_btn.pack(pady=1, fill='x')
        self.mask_btn = tk.Button(right_frame, text='Mask Image', command=self.mask_image)
        self.mask_btn.pack(pady=1, fill='x')
        self.image_index = tk.IntVar(value=0)
        self.combo = tk.Spinbox(right_frame, textvariable=self.image_index, command=self.change_image)
        self.combo.pack(pady=1, fill='x')
        tk.Entry(minmax_frame, textvariable=self.max_height, width=4).pack(side="left", padx=2)
        tk.Entry(minmax_frame, textvariable=self.max_width, width=4).pack(side="left", padx=2)

        

    def change_image(self):
        val = self.image_index.get()
        img = self.image
        match val:
            case 0:
                img = self.original_image if hasattr(self, "original_image") else self.image
            case 1:
                img = self.optimized_image if hasattr(self, "optimized_image") else self.image
            case 2:
                img = self.extruded_image if hasattr(self, "extruded_image") else self.image
            case 3:
                img = self.segmented_image if hasattr(self, "segmented_image") else self.image
            case 4:
                img = self.filtred_image if hasattr(self, "filtred_image") else self.image
            case 5:
                img = self.masked_image if hasattr(self, "masked_image") else self.image
        self.display_image(img)

    def mask_image(self):
        if hasattr(self, 'segments') and self.segments is not None:
            img = i.mask_image(self.image, self.filtred)
            self.masked_image = img
            self.display_image(img)

    def filter_segmentation(self):
        if hasattr(self, 'segments') and self.segments is not None:
            minmax = (self.min_height.get(), self.max_height.get())
            self.filtred = i.filter_segments(self.segments, minmax, self.max_width.get())
            img = i.draw_segments(self.image.size, self.filtred)
            self.display_image(img)
            self.filtred_image = img



    def show_segmentation_diagram(self):
        if hasattr(self, 'segments') and self.segments is not None:
            i.show_segments_bar_diagram(self.segments)

    def convert_to_1_mode(self):
        if hasattr(self, 'image') and self.image is not None:
            bw_image = self.image.convert('1')
            self.display_image(bw_image)

    def segment_image(self):
        import image as i
        img = self.image
        # You can adjust min_size and max_size as needed
        segments = i.segmentize_image(img)
        self.segments = segments
        seg_img = i.draw_segments(img.size, segments)
        self.display_image(seg_img)
        self.segmented_image = seg_img

    def save_image(self):
        # Save the currently displayed image
        if hasattr(self, 'image') and self.image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('JPEG files', '*.jpg'), ('All files', '*.*')])
            if file_path:
                img_to_save = self.image
                img_to_save.save(file_path)

    def load_image(self):
        file_name = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp')])
        if file_name:
            self.image_path = file_name
            self.zoom_level = 1.0
            self.original_image = Image.open(self.image_path)
            self.display_image(self.original_image)

    def display_image(self, image):
        # Convert to 'L' for display if image is in mode '1'
        if image.mode == '1':
            image = image.convert('L')
        self.image = image
        # Zoom bo'yicha resize
        w, h = image.size
        zoomed_w = int(w * self.zoom_level)
        zoomed_h = int(h * self.zoom_level)
        resized_image = image.resize((zoomed_w, zoomed_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized_image)
        self.canvas.delete('all')
        self.canvas_img = self.canvas.create_image(self.pan_offset[0], self.pan_offset[1], anchor='nw', image=self.tk_img, tags='img')
        self.canvas.config(scrollregion=(0, 0, zoomed_w, zoomed_h))
        # Update image mode label
        self.image_mode_label.config(text=f'Image Mode: {image.mode}')
        # BBOX rectni qayta chizish
        self.update()

    def start_pan(self, event):
        self.pan_start = (event.x, event.y)

    def do_pan(self, event):
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.canvas.move('img', dx, dy)
            self.pan_offset[0] += dx
            self.pan_offset[1] += dy
            self.pan_start = (event.x, event.y)

    def restore_image(self):
        self.pan_offset = [0, 0]
        self.zoom_level = 1.0
        self.display_image(self.original_image)

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 0.2, 5.0)
        self.display_image(self.original_image)

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 0.2, 0.2)
        self.display_image(self.original_image)

    def optimize_image(self):
        image = self.image
        colorizer_factors = (
            self.colorizer_r.get(),
            self.colorizer_g.get(),
            self.colorizer_b.get()
        )
        luminancer_weights = (
            self.luminancer_r.get(),
            self.luminancer_g.get(),
            self.luminancer_b.get()
        )
        binarize_value = i.percenter(255, self.threshold.get())
        sequence = [i.colorizer, i.luminancer, i.binarizer]
        args = [colorizer_factors, luminancer_weights, (binarize_value,)]
        self.optimized_image = i.sequence_optimizer(image, "RGB", "L", sequence, args)
        self.display_image(self.optimized_image)

    def extrude_image(self):
        fx, fy = self.extrude_pixel_w.get(), self.extrude_pixel.get()
        extruded_image = i.extrude_image(self.image, (fx, fy))
        self.display_image(extruded_image)
        self.extruded_image = extruded_image


    def clip_image(self):
        x1 = self.bbox_x1.get()
        y1 = self.bbox_y1.get()
        x2 = self.bbox_x2.get()
        y2 = self.bbox_y2.get()
        
        self.bbox_label.config(text=f'BBOX: ({x1}, {y1}) - ({x2}, {y2})')
        # Rasmni crop qilish
        if hasattr(self, 'image'):
            left, top = min(x1, x2), min(y1, y2)
            right, bottom = max(x1, x2), max(y1, y2)
            cropped = self.image.crop((left, top, right, bottom))
            self.display_image(cropped)

    def draw_bbox_rect(self):
        x1 = self.bbox_x1.get()
        y1 = self.bbox_y1.get()
        x2 = self.bbox_x2.get()
        y2 = self.bbox_y2.get()

        if hasattr(self, 'image'):
            draw = ImageDraw.Draw(self.image)
            draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
            self.display_image(self.image)
        
    def flip_image(self):
        if hasattr(self, 'image') and self.image is not None:
            flipped = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image(flipped)
            self.image = flipped
        

if __name__ == '__main__':
    app = ImageOptimizerGUI()
    app.mainloop()
