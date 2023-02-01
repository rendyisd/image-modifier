import tkinter as tk
import cv2
import numpy as np

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageModifierApp:
    def __init__(self, root):
        self.current_modified_image = ModifiedImage()

        self.placeholder_img = Image.new(mode = "L", size = (300, 300), color = "gray")
        self.placeholder_img = ImageTk.PhotoImage(self.placeholder_img)

        self.label_img = tk.Label(root, image = self.placeholder_img)
        self.label_img.pack(padx= 10, pady=10)

        self.button_open_img = tk.Button(root, text = "Select Image", command = self.open_image_btn)
        self.button_open_img.pack(pady=5)

        self.button_save_img = tk.Button(root, text = "Save Image", command = self.save_image_btn)
        self.button_save_img.pack(pady=5)

        self.button_threshold_img = tk.Button(root, text= "Binary Threshold Toggle", command = self.binary_threshold_toggle_btn)
        self.button_threshold_img.pack(pady=5)

        self.slider_brightness = tk.Scale(
            root, 
            from_ = 0, 
            to = 2, 
            orient = "horizontal", 
            length = 300, 
            resolution = 0.1, 
            command = self.change_brightness_slider
        )
        self.slider_brightness.set(1)
        self.slider_brightness.pack()

    def __update_label(self):
        self.label_img.config(image = self.current_modified_image.img_for_display)
        self.label_img.image = self.current_modified_image.img_for_display

    def open_image_btn(self):
        self.current_modified_image.open_image()

        try:
            self.__update_label()
        except:
            return

    def binary_threshold_toggle_btn(self):
        self.current_modified_image.binary_threshold_toggle()
        self.__update_label()
    
    def save_image_btn(self):
        self.current_modified_image.save_image()

    def change_brightness_slider(self, val):
        self.current_modified_image.change_brightness(val)
        self.__update_label()
    

class ModifiedImage:
    def __init__(self):
        self.file_path = ""
        self.img = None
        self.img_for_display = None

        self.brightness_value = 1
        self.is_binary_threshold = False

    def __apply_change(self):
        try:
            tmp_img = cv2.convertScaleAbs(self.img, alpha = self.brightness_value, beta = 0)

            if self.is_binary_threshold:
                _, tmp_img = cv2.threshold(tmp_img, 128, 255, cv2.THRESH_BINARY)
            
            self.img_for_display = self.__array_to_photoimage(tmp_img)

            return tmp_img
        except:
            messagebox.showerror("Error!", "No image selected!")

    def __array_to_photoimage(self, img_array):
        img_array = Image.fromarray(np.uint8(img_array))
        img_array = ImageTk.PhotoImage(img_array)

        return img_array
    
    def open_image(self):
        tmp_file_path = filedialog.askopenfilename()

        if tmp_file_path:
            self.file_path = tmp_file_path

            self.img = cv2.imread(self.file_path, cv2.IMREAD_ANYCOLOR)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.img = cv2.resize(self.img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)

            self.img_for_display = self.__array_to_photoimage(self.img)
    
    def save_image(self):
        file_name = self.file_path.split('/')[-1]
        file_ext = file_name[file_name.find('.')+1:]
        file_name = file_name[:file_name.find('.')]

        final_img = self.__apply_change()

        try:
            final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{file_name}_modified.{file_ext}", final_img)
            messagebox.showinfo("Success!", "The image has been saved succesfully")
        except:
            return

    def binary_threshold_toggle(self):
        if self.img is not None:
            self.is_binary_threshold = not self.is_binary_threshold

        # This will call messagebox error if img is not loaded yet
        self.__apply_change()

    def change_brightness(self, val):
        if self.img is not None:
            self.brightness_value = float(val)
            self.__apply_change()


def main():
    root = tk.Tk()
    root.title("Image Modifier")
    app = ImageModifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()