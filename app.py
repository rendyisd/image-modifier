import cv2
import numpy as np
import tkinter as tk

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageModifierApp:
    def __init__(self, root):
        self.current_modified_image = ModifiedImage()

        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)

        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)

        self.placeholder_img = Image.new(mode = "L", size = (300, 300), color = "gray")
        self.placeholder_img = ImageTk.PhotoImage(self.placeholder_img)

        # self.label_img = tk.Label(self.frame1, image = self.placeholder_img)
        # self.label_img.pack()

        self.image_canvas = tk.Canvas(self.frame1, width=300, height=300)
        self.image_canvas.pack()
        self.image_canvas.create_image(
            0, 0, 
            image=self.placeholder_img,
            anchor=tk.NW
        )

        self.button_open_img = tk.Button(self.frame2, text = "Select Image", command = self.open_image_btn)
        self.button_open_img.grid(row=0, column=0, pady=10)

        self.button_save_img = tk.Button(self.frame2, text = "Save Image", command = self.save_image_btn)
        self.button_save_img.grid(row=0, column=1)

        self.button_threshold_img = tk.Button(self.frame2, text= "Binary Threshold Toggle", command = self.binary_threshold_toggle_btn)
        self.button_threshold_img.grid(row=1, column=0, columnspan=2)
        
        self.button_flip_horizontal = tk.Button(self.frame2, text= "Horizontal Flip", command = lambda : self.flip_image_btn(1))
        self.button_flip_horizontal.grid(row=2, column=0, pady=10)

        self.button_flip_vertical = tk.Button(self.frame2, text= "Vertical Flip", command = lambda : self.flip_image_btn(0))
        self.button_flip_vertical.grid(row=2, column=1)

        self.slider_brightness_text_label = tk.Label(self.frame2, text="Brightness")
        self.slider_brightness_text_label.grid(row=3, column=0, columnspan=2)
        self.slider_brightness = tk.Scale(
            self.frame2, 
            from_ = 0, 
            to = 2, 
            orient = "horizontal", 
            length = 200, 
            resolution = 0.1, 
            command = self.change_brightness_slider
        )
        self.slider_brightness.set(1)
        self.slider_brightness.grid(row=4, column=0, columnspan=2)

        self.slider_rotate_text_label = tk.Label(self.frame2, text="Rotation Degree")
        self.slider_rotate_text_label.grid(row=5, column=0, columnspan=2)
        self.slider_rotate = tk.Scale(
            self.frame2, 
            from_ = -180, 
            to = 180, 
            orient = "horizontal", 
            length = 200, 
            resolution = 1, 
            command = self.rotate_image_slider
        )
        self.slider_rotate.grid(row=6, column=0, columnspan=2)

    def __update_canvas(self):
        self.image_canvas.delete("all")
        if self.current_modified_image.img is not None:
            self.image_canvas.config(
                width = self.current_modified_image.img.shape[1],
                height = self.current_modified_image.img.shape[0]
            )
        self.image_canvas.create_image(
            0, 0, 
            image=self.current_modified_image.img_for_display,
            anchor=tk.NW
        )

    def open_image_btn(self):
        self.current_modified_image.open_image()

        try:
            self.__update_canvas()
        except:
            return
    
    def save_image_btn(self):
        self.current_modified_image.save_image()

    def binary_threshold_toggle_btn(self):
        self.current_modified_image.binary_threshold_toggle()
        self.__update_canvas()
    
    def flip_image_btn(self, mode : int):
        self.current_modified_image.flip_image(mode)
        self.__update_canvas()
    
    def change_brightness_slider(self, val):
        self.current_modified_image.change_brightness(val)
        self.__update_canvas()
    
    def rotate_image_slider(self, degree):
        self.current_modified_image.rotate_image(degree)
        self.__update_canvas()

class ModifiedImage:
    def __init__(self):
        self.file_path = ""
        self.img = None
        self.img_for_display = None

        self.is_binary_threshold = False
        self.brightness_value = 1
        self.rotate_degree = 0

    def __apply_change(self):
        try:
            rows, cols = self.img.shape[:2]
            rotation_M = cv2.getRotationMatrix2D((cols / 2, rows / 2), self.rotate_degree, 1)

            tmp_img = cv2.convertScaleAbs(self.img, alpha = self.brightness_value, beta = 0)
            tmp_img = cv2.warpAffine(tmp_img, rotation_M, (cols, rows))
            
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
            # self.img = cv2.resize(self.img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)

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

        # This will call messagebox error if img hasnt been loaded yet
        self.__apply_change()

    def flip_image(self, mode):
        if self.img is not None:
            self.img = cv2.flip(self.img, mode)
        self.__apply_change()
    
    def change_brightness(self, val):
        if self.img is not None:
            self.brightness_value = float(val)
            self.__apply_change()

    def rotate_image(self, degree):
        if self.img is not None:
            self.rotate_degree = int(degree)
            self.__apply_change()
        

def main():
    root = tk.Tk()
    root.title("Image Modifier")
    app = ImageModifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()