
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TimelineViewer:
    def __init__(self, root, image_folder):
        # list pngs
        self.root = root
        self.image_folder = image_folder
        self.images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png'))]
        self.current_image_index = 0

        # create image display
        self.image_label = tk.Label(root)
        self.image_label.pack(padx=10, pady=10)

        # create slider with tick for each image
        self.slider = ttk.Scale(root, from_=0, to=len(self.images) - 1, orient="horizontal", command=self.update_image)
        self.slider.pack(fill="both", padx=10, pady=10)
        self.update_image()

    def update_image(self, event=None):
        """updages image label to display image respective to image slider tick"""
        self.current_image_index = int(self.slider.get())
        image_path = os.path.join(self.image_folder, self.images[self.current_image_index])
        image = Image.open(image_path)
        image = image.resize((750, 500), resample=Image.NEAREST)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Slider")

    image_folder = "data/real_timeline"
    app = TimelineViewer(root, image_folder)

    root.mainloop()
