# -*- coding: utf-8 -*-
import tkinter as tk

class PFFrame(tk.Frame):
    '''Frame personalizado com a imagem da PF como plano de fundo
    '''
    def __init__(self, frame_master : tk.Frame, shift_y : int):
        image_pf = tk.PhotoImage(file="imagens/aavia.png")
        super().__init__(frame_master, width=(frame_master.winfo_reqwidth() - shift_y), 
                         height=frame_master.winfo_reqheight(), bg="white")
        
        self.label_pf = tk.Label(self, image=image_pf, bg="white")
        self.label_pf.image = image_pf
        self.shift_y = shift_y
        
    def pack(self):
        h_screen = self.winfo_screenheight()
        w_screen = self.winfo_screenwidth()
        
        h_photo = self.label_pf.winfo_reqheight()
        w_photo = self.label_pf.winfo_reqwidth()
        
        _x = (w_screen - w_photo)/2
        _y = (h_screen - self.shift_y - h_photo )/2
        if(_y < 0):
            _y = 0
        
        super().place(x=_x, y=_y + self.shift_y)
        self.label_pf.pack(anchor="center")

