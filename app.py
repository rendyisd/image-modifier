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

        self.image_canvas = tk.Canvas(self.frame1, width=960, height=540)
        self.image_canvas.pack()

        self.button_open_img = tk.Button(self.frame2, text = "Select Image", command = self.open_image_btn)
        self.button_open_img.grid(row=0, column=0, pady=(0, 10))

        self.button_save_img = tk.Button(self.frame2, text = "Save Image", command = self.save_image_btn)
        self.button_save_img.grid(row=0, column=1, pady=(0, 10))

        self.button_threshold_img = tk.Button(self.frame2, text= "Binary Threshold Toggle", command = self.binary_threshold_toggle_btn)
        self.button_threshold_img.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.button_grayscale_img = tk.Button(self.frame2, text= "Grayscale Toggle", command = self.grayscale_toggle_btn)
        self.button_grayscale_img.grid(row=2, column=0, columnspan=2, pady = (0, 10))
        
        self.button_flip_horizontal = tk.Button(self.frame2, text= "Horizontal Flip", command = lambda : self.flip_image_btn(1))
        self.button_flip_horizontal.grid(row=3, column=0, pady=(0, 10))

        self.button_flip_vertical = tk.Button(self.frame2, text= "Vertical Flip", command = lambda : self.flip_image_btn(0))
        self.button_flip_vertical.grid(row=3, column=1, pady=(0, 10))

        self.slider_brightness_text_label = tk.Label(self.frame2, text="Brightness")
        self.slider_brightness_text_label.grid(row=4, column=0, columnspan=2)
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
        self.slider_brightness.grid(row=5, column=0, columnspan=2)

        self.slider_rotate_text_label = tk.Label(self.frame2, text="Rotation Degree")
        self.slider_rotate_text_label.grid(row=6, column=0, columnspan=2)
        self.slider_rotate = tk.Scale(
            self.frame2, 
            from_ = -180, 
            to = 180, 
            orient = "horizontal", 
            length = 200, 
            resolution = 1, 
            command = self.rotate_image_slider
        )
        self.slider_rotate.grid(row=7, column=0, columnspan=2)

        self.slider_rescale_text_label = tk.Label(self.frame2, text="Image Size Multiplier")
        self.slider_rescale_text_label.grid(row=8, column=0, columnspan=2)
        self.slider_rescale = tk.Scale(
            self.frame2, 
            from_ = 0.5, 
            to = 1.5, 
            orient = "horizontal", 
            length = 200, 
            resolution = 0.1, 
            command = self.rescale_image_slider
        )
        self.slider_rescale.set(1)
        self.slider_rescale.grid(row=9, column=0, columnspan=2)

        self.button_sharpen_img = tk.Button(self.frame2, text= "Sharpen Toggle", command = self.sharpen_toggle_btn)
        self.button_sharpen_img.grid(row=10, column=0, columnspan=2, pady=(10, 0))

        self.button_deblur_img = tk.Button(self.frame2, text= "Deblur Toggle", command = self.deblur_toggle_btn)
        self.button_deblur_img.grid(row=11, column=0, columnspan=2, pady=(10, 0))

        self.button_sobel_ed_img = tk.Button(self.frame2, text= "Sobel ED Toggle", command = self.sobel_ed_toggle_btn)
        self.button_sobel_ed_img.grid(row=12, column=0, columnspan=2, pady=(10, 0))


    def __update_canvas(self):
        self.image_canvas.delete("all")

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        multiplier = 1 if self.current_modified_image.rescale_multiplier > 1 else self.current_modified_image.rescale_multiplier
        image_width = int(self.current_modified_image.img_display_width * multiplier)
        image_height = int(self.current_modified_image.img_display_height * multiplier)
        try:
            self.image_canvas.create_image(
                center_x - (image_width // 2),
                center_y - (image_height // 2), 
                image=self.current_modified_image.img_display,
                anchor=tk.NW
            )
        except:
            return

    def open_image_btn(self):
        self.current_modified_image.open_image(
            self.image_canvas.winfo_width(),
            self.image_canvas.winfo_height()
        )

        self.__update_canvas()
    
    def save_image_btn(self):
        self.current_modified_image.save_image()

    def binary_threshold_toggle_btn(self):
        self.current_modified_image.binary_threshold_toggle()
        self.__update_canvas()
    
    def grayscale_toggle_btn(self):
        self.current_modified_image.grayscale_toggle()
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

    def rescale_image_slider(self, multiplier):
        self.current_modified_image.rescale_image(multiplier)
        self.__update_canvas()

    def sharpen_toggle_btn(self):
        self.current_modified_image.sharpen_toggle()
        self.__update_canvas()
    
    def deblur_toggle_btn(self):
        self.current_modified_image.deblur_toggle()
        self.__update_canvas()
    
    def sobel_ed_toggle_btn(self):
        self.current_modified_image.sobel_ed_toggle()
        self.__update_canvas()
        

class ModifiedImage:
    def __init__(self):
        self.file_path = ""

        self.img = None
        self.img_width = 0
        self.img_height = 0

        self.img_display = None
        self.img_display_width = 0
        self.img_display_height = 0

        self.is_binary_threshold = False
        self.is_grayscale = False
        self.is_sharpen = False
        self.is_deblur = False
        self.is_sobel_ed = False

        self.brightness_value = 1
        self.rotate_degree = 0
        self.rescale_multiplier = 1

    def __apply_change(self):
        try:
            rows, cols = self.img.shape[:2]
            rotation_M = cv2.getRotationMatrix2D((cols / 2, rows / 2), self.rotate_degree, 1)

            # Apply change brightness
            tmp_img = cv2.convertScaleAbs(self.img, alpha = self.brightness_value, beta = 0)

            # Apply rotate image
            tmp_img = cv2.warpAffine(tmp_img, rotation_M, (cols, rows))
            
            # Apply binary threshold
            if self.is_binary_threshold:
                _, tmp_img = cv2.threshold(tmp_img, 128, 255, cv2.THRESH_BINARY)
            
            # Apply grayscale
            if self.is_grayscale:
                tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
            
            # Apply sharpen
            if self.is_sharpen:
                kernel = np.array([[0, -1, 0],
                                    [-1, 5, -1],
                                    [0, -1, 0]])
                tmp_img = self.__convolution(tmp_img, kernel)
            
            # Apply deblur

            # Apply soble edge detection
            
            # Prepare the image for display which includes resizing the displayed image
            self.img_display = self.__array_to_photoimage_resize(tmp_img)

            return tmp_img
        except:
            messagebox.showerror("Error!", "No image selected!")

    def __array_to_photoimage_resize(self, img_array):
        img_array = Image.fromarray(np.uint8(img_array))
        multiplier = 1 if self.rescale_multiplier > 1 else self.rescale_multiplier
        
        img_array = img_array.resize((
            int(self.img_display_width * multiplier),
            int(self.img_display_height * multiplier)
        ))

        img_array = ImageTk.PhotoImage(img_array)

        return img_array

    def __convolution(self, img : np.ndarray, kernel : np.ndarray):
        # Grayscale image only
        img_rows, img_cols = img.shape
        kernel_rows, kernel_cols = kernel.shape
        
        res_rows = img_rows - kernel_rows + 1
        res_cols = img_cols - kernel_cols + 1
        
        img_res = np.zeros((res_rows, res_cols))
        
        max_grayness = np.amax(img)
        for i in range(res_rows):
            for j in range(res_cols):
                img_res[i][j] = np.clip(
                    np.sum(img[i : i+kernel_rows, j : j+kernel_cols] * kernel),
                    0, max_grayness
                )
        
        return img_res
    
    def open_image(self, canvas_width, canvas_height):
        tmp_file_path = filedialog.askopenfilename()

        if tmp_file_path:
            self.file_path = tmp_file_path

            self.img = cv2.imread(self.file_path, cv2.IMREAD_ANYCOLOR)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

            self.img_height, self.img_width = self.img.shape[:2]
            self.img_display_height, self.img_display_width = self.img.shape[:2]
            aspect_ratio = self.img_display_width / self.img_display_height

            # Scale to fit the canvas
            if(self.img_display_width > canvas_width):
                self.img_display_width = canvas_width
                self.img_display_height = int(self.img_display_width / aspect_ratio)
            
            if(self.img_display_height > canvas_height):
                self.img_display_height = canvas_height

            self.img_display = self.__array_to_photoimage_resize(self.img)

    def save_image(self):
        file_name = self.file_path.split('/')[-1]
        file_ext = file_name[file_name.find('.')+1:]
        file_name = file_name[:file_name.find('.')]

        final_img = self.__apply_change()

        # Apply image rescale
        final_img = cv2.resize(
            final_img,
            (
                int(self.img_width * self.rescale_multiplier),
                int(self.img_height * self.rescale_multiplier)
            ),
            interpolation=cv2.INTER_CUBIC
        )

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
    
    def grayscale_toggle(self):
        if self.img is not None:
            self.is_grayscale = not self.is_grayscale
        
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

    def rescale_image(self, multiplier):
        if self.img is not None:
            self.rescale_multiplier = float(multiplier)
            self.__apply_change()
    
    def sharpen_toggle(self):
        if self.img is not None:
            self.is_sharpen = not self.is_sharpen
        self.__apply_change()

    def sharpen_toggle(self):
        if self.img is not None:
            self.is_deblur = not self.is_deblur
        self.__apply_change()
    
    def sobel_ed_toggle(self):
        if self.img is not None:
            self.is_sobel_ed = not self.is_sobel_ed
        self.__apply_change()
        

def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("+50+50")
    root.title("Image Modifier")

    app = ImageModifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()