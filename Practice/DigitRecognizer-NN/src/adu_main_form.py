import tkinter as tk
from tkinter import Canvas

import image_processing
import mnist_loader
import network
import numpy as np
from PIL import Image, ImageDraw, ImageTk

# Rasm o‘lchami
IMAGE_SIZE = 256
model_path = "models/adu_mnist.pkl.gzip"

class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Qo'lda raqam chizish va aniqlash")

        self.model = mnist_loader.load_data(model_path)

        # Asosiy Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Chap tomonda - Chizish maydoni
        self.canvas = Canvas(self.main_frame, width=IMAGE_SIZE, height=IMAGE_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=12, padx=10, pady=5)
        self.canvas.bind("<B1-Motion>", self.draw)

        # 28x28 rasmni ko'rsatish maydoni
        self.img_label = tk.Label(self.main_frame)
        self.img_label.grid(row=0, column=1, padx=10, pady=5)

        # O‘ng tomonda - Tugmalar va natijalar
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.grid(row=1, column=1, padx=10)

        # Aniqlash tugmasi
        self.predict_button = tk.Button(self.control_frame, text="Aniqlash", command=self.predict_digit, font=("Arial", 12))
        self.predict_button.pack(pady=5)

        # Natija chiqarish labeli
        self.result_label = tk.Label(self.control_frame, text="Aniqlangan raqam: ?", font=("Arial", 14))
        self.result_label.pack(pady=5)

        # 0-9 raqamlar uchun ehtimollik labellari
        self.prob_labels = []
        for i in range(10):
            lbl = tk.Label(self.control_frame, text=f"{i}: ?", font=("Arial", 12), anchor="w")
            lbl.pack(fill="both")
            self.prob_labels.append(lbl)

        # Tozalash tugmasi
        self.clear_button = tk.Button(self.control_frame, text="Tozalash", command=self.clear_canvas, font=("Arial", 12))
        self.clear_button.pack(pady=10)

        # Grayscale nazorat qilish slayderi
        self.gray_scale_value = tk.IntVar(value=0)  # 0 - qora, 255 - oq
        self.gray_slider = tk.Scale(self.control_frame, from_=0, to=255, orient="horizontal", label="Grayscale", variable=self.gray_scale_value, command=self.update_grayscale)
        self.gray_slider.pack(pady=5)

        # Rasmni saqlash uchun oq fonli PIL Image
        self.image = Image.new("L", (IMAGE_SIZE, IMAGE_SIZE), 255)
        self.draw_image = ImageDraw.Draw(self.image)

    def draw(self, event):
        """Chizish funksiyasi."""
        x, y = event.x, event.y
        r = 5  # Qalam qalinligi
        color = self.gray_scale_value.get()
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=f"#{color:02x}{color:02x}{color:02x}", outline=f"#{color:02x}{color:02x}{color:02x}")
        self.draw_image.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def clear_canvas(self):
        """Chizish maydonini tozalash."""
        self.canvas.delete("all")
        self.image = Image.new("L", (IMAGE_SIZE, IMAGE_SIZE), 255)
        self.draw_image = ImageDraw.Draw(self.image)
        self.result_label.config(text="Aniqlangan raqam: ?")
        self.img_label.config(image="")  # 28x28 rasmni ham tozalash
        for lbl in self.prob_labels:
            lbl.config(text=f"{lbl.cget('text').split(':')[0]}: ?")

    def update_grayscale(self, event=None):
        """Slayderni harakatlantirganda chizilgan rasmga ta’sir qiladi."""
        pass  # Chizish funksiyasi allaqachon slider qiymatini ishlatadi

    def predict_digit(self):
        """Rasmni model uchun tayyorlash va natija chiqarish."""
        # Rasmni 28x28 formatga moslashtirish
        img_resized = self.image.resize((28, 28)).convert("RGB")
        pixels = np.asarray(image_processing.color_convert_image(img_resized)).flatten()

        # 28x28 rasmini ekranga chiqarish
        img_tk = ImageTk.PhotoImage(Image.fromarray(pixels.reshape(28, 28), mode="L"))
        self.img_label.config(image=img_tk)
        self.img_label.image = img_tk

        # Rasmni neyron tarmoq uchun tayyorlash
        img_array = image_processing.normalize_values(pixels)

        # Model yordamida bashorat qilish
        predicts = network.predict(self.model, img_array)
        predicted_digit = np.argmax(predicts)

        # Natijalarni chiqarish
        self.result_label.config(text=f"Aniqlangan raqam: {predicted_digit}")
        for i, lbl in enumerate(self.prob_labels):
            lbl.config(text=f"{i}: {predicts[i]:.5f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()
