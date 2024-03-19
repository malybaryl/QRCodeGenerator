import tkinter as tk
import customtkinter as ctk
import scripts.variables
import qrcode
from PIL import Image, ImageTk
from os import walk
from tkinter import filedialog
from scripts.loadfolders import load_folders
from scripts.loadconfig import load_config
from scripts.saveconfig import save_config

class App(ctk.CTk):
    def __init__(self):
        global config_file
        config_file, dark_mode, geometry = load_config()
        if dark_mode:
            mode = 'dark'
            scripts.variables.DARKMODE = True
        else: 
            mode = 'light'
            scripts.variables.DARKMODE = False
            
        if scripts.variables.LANGUAGE == 'PL':
            entry_start_value = 'Wpisz tutaj tekst, który chesz wygenerować'
        else:
            entry_start_value = 'Enter the text you want to generate here'
        
        # window setup
        ctk.set_appearance_mode(mode)
        super().__init__()
        self.title('')
        self.iconbitmap('assets/icon/0.ico')
        self.minsize(400,400)
        self.geometry(geometry)
        
        # QR code image
        self.raw_image = None
        self.tk_image = None
        
        # widgets
        self.entry_string = ctk.StringVar(value= entry_start_value)
        self.entry_string.trace('w', self.create_qr)
        self.qr_image = QrImage(self)
        self.qr_image.update_image(self.tk_image)
        EntryField(self, config_file, self.entry_string)
        
        # binds
        self.bind_all('<Configure>', self.trigger_bind_configure)
        self.bind('<Return>', self.save_qr)
        # run
        self.mainloop()
        
    def trigger_bind_configure(self, *args):
        self.after(10000, self.save_geometry)
    
    def save_geometry(self):
        width = self.winfo_width()
        height = self.winfo_height()
        config_file[3] = str(width)
        config_file[5] = str(height)
        
        save_config(config_file)
        
    def import_config_file_from_other_class(self, file):
        config_file = file
        
        self.save_geometry()
        
    def create_qr(self, *args):
        current_text = self.entry_string.get()
        if current_text:
            self.raw_image = qrcode.make(current_text).resize((400,400))
            self.tk_image = ImageTk.PhotoImage(self.raw_image)
            self.qr_image.update_image(self.tk_image)
        else:
            self.qr_image.clear()
            self.raw_image = None
            self.tk_image = None
            
    def save_qr(self, event = ''):
        if self.raw_image:
            file_path = filedialog.asksaveasfilename()
            
        if file_path:
            self.raw_image.save(file_path + '.png')
            
        
            
         
class ModeButton(ctk.CTkButton):
    def __init__(self, parent, config_file):
        self.parent = parent
        self.config_file_ = config_file
          
        # animation logic setup
        self.frames = load_folders('assets/mode','assets/mode')
        self.animation_length = len(self.frames) - 1
        if scripts.variables.DARKMODE:
            self.animation_status = ctk.StringVar(value = 'dark')
            self.frame_index = 0
            #scripts.variables.DARKMODE_CANVAS = True
        else:
            self.animation_status = ctk.StringVar(value = 'light')
            self.frame_index = self.animation_length
            #scripts.variables.DARKMODE_CANVAS = False
        self.animation_status.trace('w', self.change_mode)
            
        super().__init__(
            master = self.parent,
            text= '',
            image = self.frames[self.frame_index],
            width = 32,
            height = 32,
            corner_radius= 1,
            fg_color = 'transparent',
            hover= False,
            command = self.trigger_button)
          
     
    def trigger_button(self):
        if self.animation_status.get() == 'dark':
            self.frame_index = 0
            self.animation_status.set('forward')
            ctk.set_appearance_mode('light')
            self.config_file_[1] = 'no'
            self.parent.import_config_file_from_other_class(self.config_file_)
            scripts.variables.DARKMODE_CANVAS = False
            #self.parent.qr_image.configure(bg= '#242424')
            
            
        if self.animation_status.get() == 'light':
            self.frame_index = self.animation_length
            self.animation_status.set('backward')
            ctk.set_appearance_mode('dark')
            self.config_file_[1] = 'yes'
            self.parent.import_config_file_from_other_class(self.config_file_)  
            scripts.variables.DARKMODE_CANVAS = True
            #self.parent.qr_image.configure(bg= '#EBEBEB')
            
            
            
        
    def change_mode(self, *args):
        if self.animation_status.get() == 'forward':
            self.frame_index += 1
            self.configure(image = self.frames[self.frame_index]) 
            if self.frame_index < self.animation_length: 
                self.after(20, self.change_mode)  
            else:
                self.animation_status.set('light')
        
        if self.animation_status.get() == 'backward':
            self.frame_index -= 1
            self.configure(image = self.frames[self.frame_index]) 
            if self.frame_index > 0: 
                self.after(20, self.change_mode)  
            else:
                self.animation_status.set('dark')
                
class Entry(ctk.CTkEntry):
    def __init__(self, parent, entry_string):
        super().__init__(parent,
                         border_color= ('#039eff','#3c029c'),
                         border_width= 2,
                         textvariable= entry_string)

class Button(ctk.CTkButton):
    def __init__(self, parent, app):
        if scripts.variables.LANGUAGE == 'PL':
            text = 'ZAPISZ'
        else:
            text = 'SAVE'
        super().__init__(parent,
                         text = text,
                         border_color= ('#17a5fc','#3c029c'),
                         fg_color= ('#079dfa','#5802e6'),
                         border_width= 2,
                         height= 32,
                         hover_color= ('#007bc7','#5102d4'),
                         text_color= ('black', 'white'),
                         font=('',16),
                         command= app.save_qr)
                
class EntryField(ctk.CTkFrame):
    def __init__(self, parent, config_file, entry_string):
        
        super().__init__(parent,
                         fg_color= ('#007bc7','#4c00c7'),
                         border_width = 10,
                         border_color= ('#039eff','#3c029c'),
                         corner_radius= 20)
        self.anchor = 'nw'
        self.y = 1
        self.animate()
        
        self.frame = ctk.CTkFrame(self, fg_color= 'transparent')
        
        
            
        mode_button = ModeButton(self.frame, config_file)
        entry = Entry(self.frame, entry_string)
        button = Button(self.frame, parent)
            
        mode_button.pack(side = 'left', padx = 2)
        entry.pack(side = 'left', padx = 2, expand = True, fill = 'both')
        button.pack(side = 'left', padx = 2)
            
        self.frame.place(relx = 0.5, rely = 0.3, anchor = 'center', relwidth = 0.8)
            
            
        
        
    def animate(self):
        if self.y >= 0.8:
            self.y -= 0.01
            self.frame = ctk.CTkFrame(self, fg_color= 'transparent')
            self.place(anchor = self.anchor, x= 0, rely = self.y, relwidth = 1, relheight = 0.4)
            self.after(15, self.animate)
        
            
        
        
            
        
        
class QrImage(tk.Canvas):
    def __init__(self, parent):
        
        super().__init__(master= parent,
                            highlightthickness= 0,
                            relief= 'ridge',
                            bg= ('#EBEBEB'))
        
        self.place(relx = 0.5, rely = 0.4, width= 400, height=400, anchor= 'center')
        
    def update_image(self, image_tk):
        self.clear()
        self.create_image(0, 0, image = image_tk, anchor = 'nw')
        
    def clear(self):
        self.delete('all')
        
    
def main():
    App()

if __name__ == "__main__":
    main()