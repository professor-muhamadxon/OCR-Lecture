"""import numpy as np
import matplotlib.pyplot as plt

# Har bir raqam uchun 100 ta 84x84 tasvirlarni tasodifiy yaratamiz
data = {i: np.random.rand(100, 84, 84) for i in range(10)}

# Har bir raqam uchun o'rtacha issiqlik xaritasini hisoblash
average_data = {i: np.mean(data[i], axis=0) for i in range(10)}

fig, axes = plt.subplots(2, 5, figsize=(15, 8), constrained_layout=True)
fig.suptitle("Average Heatmaps for Digits 0-9", fontsize=16)

for i, ax in enumerate(axes.flat):
    im = ax.imshow(average_data[i], cmap="coolwarm")
    ax.set_title(f"Digit {i}")
    ax.axis("off")

fig.colorbar(im, ax=axes[:, -1], shrink=0.6)
plt.show()"""


import tkinter as tk
from tkinter import Canvas
import numpy as np
from PIL import Image, ImageTk

class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Recognizer")

        # Chap tomonda chizish maydoni (128x128)
        self.canvas = Canvas(root, width=128, height=128, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)
        self.canvas.bind("<B1-Motion>", self.draw)

        # 28x28 rasm ko'rsatish maydoni
        self.img_label = tk.Label(root)
        self.img_label.grid(row=0, column=1, padx=10, pady=10)

        # "Aniqlash" tugmasi
        self.predict_btn = tk.Button(root, text="Aniqlash", command=self.process_image)
        self.predict_btn.grid(row=1, column=1, pady=5)

        # Natija label
        self.result_label = tk.Label(root, text="Natija: ?", font=("Arial", 14))
        self.result_label.grid(row=2, column=1, pady=5)

        # 0-9 raqamlar ehtimolliklarini chiqarish
        self.prob_labels = [tk.Label(root, text=f"{i}: ?", font=("Arial", 10)) for i in range(10)]
        for i, lbl in enumerate(self.prob_labels):
            lbl.grid(row=3 + i, column=1, sticky="w")

        # Rasm ma'lumotlarini saqlash uchun matritsa
        self.image_data = np.zeros((128, 128), dtype=np.uint8)

    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x + 8, y + 8, fill="black", outline="black")
        if 0 <= x < 128 and 0 <= y < 128:
            self.image_data[y, x] = 255

    def process_image(self):
        # 128x128 ni 28x28 ga o'lchamini kamaytirish
        img = Image.fromarray(self.image_data)
        img = img.resize((28, 28))

        # 28x28 rasmini ekranga chiqarish
        img_tk = ImageTk.PhotoImage(img)
        self.img_label.config(image=img_tk)
        self.img_label.image = img_tk

        # Fake neyron tarmoq chiqishi (tasodifiy ehtimollik)
        softmax_output = np.random.rand(10)
        softmax_output /= softmax_output.sum()

        # Eng katta ehtimollik qaysi son bo‘lsa, natija o‘sha bo‘ladi
        predicted_digit = np.argmax(softmax_output)
        self.result_label.config(text=f"Natija: {predicted_digit}")

        # 0-9 ehtimolliklarini chiqarish
        for i, lbl in enumerate(self.prob_labels):
            lbl.config(text=f"{i}: {softmax_output[i]:.2f}")

# Tkinter ilovani ishga tushirish
root = tk.Tk()
app = DigitRecognizerApp(root)
root.mainloop()

