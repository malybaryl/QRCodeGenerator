import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from os import walk

def load_folders(light_path, dark_path):
    image_paths = []
    for path in (light_path, dark_path):
        for folder_name, sup_folder, image_data in walk(path):
            sorted_data = sorted(image_data)
            full_path_data = [path + '/' + item for item in sorted_data]
            image_paths.append(full_path_data)
    image_paths = zip(*image_paths)
        
    ctk_images = []
    
    for image_path in image_paths:
        ctk_image = ctk.CTkImage(
            light_image = Image.open(image_path[0]),
            dark_image = Image.open(image_path[1]))
        ctk_images.append(ctk_image)

    return ctk_images