# -*- coding: utf-8 -*-
import tkinter as tk

class PFFrame(tk.Frame):
    '''Frame personalizado com a imagem da PF como plano de fundo
    '''
    def __init__(self, frame_master : tk.Frame, image_pf : tk.PhotoImage, shift_y : int):
        super().__init__(frame_master, width=(frame_master.winfo_reqwidth() - shift_y), 
                         height=frame_master.winfo_reqheight(), bg="white")
        self.label_pf = tk.Label(self, image=image_pf, bg="white")
        
    def pack(self):
        super().pack()
        self.label_pf.pack(anchor="center")

