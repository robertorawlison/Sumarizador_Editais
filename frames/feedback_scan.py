# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk

class FeedbackScan(tk.Frame):
    '''Widget personalizado para informar que a atividade está sendo processada durante o scan dos documentos e apensos
 
    '''
    def __init__(self, 
                 frame_master : tk.Frame):     
        super().__init__(frame_master, relief="solid", borderwidth=10)
        self.lift() #Frame fica por cima dos outros
        
        # Adiciona a imagem como plano de fundo usando um rótulo
        self.image = tk.PhotoImage(file="imagens/gear.png")
        self.label_gear = tk.Label(self, image=self.image)
        self.label_gear.pack(expand=True, fill="both")
             
        self._center()
                
        
    def _update_count(self):
        pass
        
    
    def update_image(self, img : Image):
        self.image = ImageTk.PhotoImage(img)
        self.label_gear.configure(image=self.image)
        self.update_idletasks() 
        self._center()
        
        self._update_count()
        
       
    def _center(self):
        ww = self.winfo_reqwidth()
        hw = self.winfo_reqheight()

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x_pos = ws // 2 - ww // 2
        y_pos = hs // 2 - hw // 2

        self.place(x=x_pos, y=y_pos)