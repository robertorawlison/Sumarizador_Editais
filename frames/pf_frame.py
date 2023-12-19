# -*- coding: utf-8 -*-
import tkinter as tk

class PFFrame(tk.Frame):
    '''Frame personalizado com a imagem da PF como plano de fundo
    '''
    def __init__(self, frame_master : tk.Frame, shift_y : int):
        image_pf = tk.PhotoImage(file="imagens/pf-cinza.png")
        super().__init__(frame_master, width=(frame_master.winfo_reqwidth() - shift_y), 
                         height=frame_master.winfo_reqheight(), bg="white")
        
        self.label_pf = tk.Label(self, image=image_pf, bg="white")
        self.label_pf.image = image_pf
        
    def pack(self):
        h_screen = self.winfo_screenheight()
        w_screen = self.winfo_screenwidth()
        
        h_photo = self.label_pf.winfo_reqheight()
        w_photo = self.label_pf.winfo_reqwidth()
        
        super().place(x=(w_screen - w_photo)/2, y=(h_screen - h_photo)/2)
        self.label_pf.pack(anchor="center")

