# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


class Button(tk.Button):
    num_instance = 0
    def __init__(self, master_frame : tk.Frame, img_file_name : str, text : str, on_click):
        self.master_frame = master_frame
        self.image = tk.PhotoImage(file=img_file_name)
        self.text = text
        self.on_click = on_click
        
        super().__init__(self.master_frame, text=self.text, image=self.image, command=self.on_click)
         
        # Associando os eventos ao botão
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
         
        self.tooltip = ttk.Label(self.master_frame, text=self.text, background="#FFFFE0", relief="solid")
        Button.num_instance += 1
        self.pos = Button.num_instance - 1 #Define a coluna que o botão ficará no grid do master_frame associado 
        
        
    def pack(self):
        self.grid(row=0, column=self.pos, pady=20, padx=10)
    
    def active(self):
        self.configure(state="normal")
    
    def disactive(self):
        self.configure(state="disabled")
 
    def on_enter(self, event):
        self.tooltip.place(in_=self, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

    def on_leave(self, event):
        self.tooltip.place_forget()
        
        
class AddButton(Button):
    """
    Botão para adição de novos documentos.
    """
    def __init__(self, master_frame : tk.Frame, on_click):
        super().__init__(master_frame, 
                     img_file_name = "imagens/add.png",
                     text = "Adicionar novos documentos periciais.",
                     on_click = on_click)
        
class CatalogButton(Button):
    """
    Botão para geração de um catálogo de documentos.
    """
    def __init__(self, master_frame : tk.Frame, on_click):
        super().__init__(master_frame, 
                     img_file_name = "imagens/catalog.png",
                     text = "Gerar catálogo de documentos periciais.",
                     on_click = on_click)

class ReportButton(Button):
    """
    Botão para geração do relatório em .doc (word).
    """
    def __init__(self, master_frame : tk.Frame, on_click):
        super().__init__(master_frame, 
                     img_file_name = "imagens/report.png",
                     text = "Gerar relatório em .doc",
                     on_click = on_click)