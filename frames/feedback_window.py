# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class FeedbackWindow(tk.Frame):
    '''Widget personalizado para informar que a atividade está sendo processada
    '''
    def __init__(self, frame_master : tk.Frame, num_docs : int):
        super().__init__(frame_master, relief="solid", borderwidth=10)
        self.lift() #Frame fica por cima dos outros
        

        # Adiciona a imagem como plano de fundo usando um rótulo
        self.image = tk.PhotoImage(file="imagens/gear.png")
        self.label_gear = tk.Label(self, image=self.image)
        self.label_gear.pack(expand=True, fill="both")
        
        #Frame para as barras de progressão
        prog_bar_frame = tk.Frame(self, relief="ridge", borderwidth=5)
        prog_bar_frame.place(relx=0.5, rely=0.5, anchor="center")
        prog_bar_frame.lift()
        
        #Barra de proresso dos documentos
        self.count_doc = 1
        self.num_docs = num_docs
        
        self.l_count_docs = tk.Label(prog_bar_frame, font = ("Arial", 15),
                                    text = "Analisando documento " + str(self.count_doc) +" de "+str(self.num_docs))
        self.l_count_docs.pack()
        
        self.prog_bar_doc = ttk.Progressbar(prog_bar_frame, orient="horizontal", length=200, mode="determinate")
        self.prog_bar_doc.pack(pady=5)
        
        self.prog_bar_doc["value"] = 0
        self.step_docs = 100 / self.num_docs
        
        
        #Barra de progresso das páginas
        self.count_page = 0
        self.num_pages = 0
        
        self.l_count_pages = tk.Label(prog_bar_frame, font = ("Arial", 15),
                                    text = "Tratando página " + str(self.count_page) +" de "+str(self.num_pages))
        self.l_count_pages.pack()
        
        self.prog_bar_page = ttk.Progressbar(prog_bar_frame, orient="horizontal", length=200, mode="determinate")
        self.prog_bar_page.pack(pady=5)
        
        
    def reset_count_pages(self, num_pages : int) -> None:
        self.count_page = 0
        self.num_pages = num_pages
        self.prog_bar_page["value"] = 0
        self.step_pages = 100 / self.num_pages
        
    def update_count_pages(self):
        self.prog_bar_page["value"] += self.step_pages
        self.count_page += 1
        self.l_count_pages.config(text="Tratando página " + str(self.count_page) +" de "+str(self.num_pages))
        
    def in_summary(self) :
        self.l_count_pages.config(text="Resumindo ...")
    
    def update_image(self, img : Image):
        self.image = ImageTk.PhotoImage(img)
        self.label_gear.configure(image=self.image)
        self.update_idletasks() 
        self.center()
        
        self.update_count_pages()
        
    
    def update_count_docs(self):
        self.prog_bar_doc["value"] += self.step_docs
        self.count_doc += 1
        self.l_count_docs.config(text="Analisando documento " + str( self.count_doc) +" de "+str(self.num_docs))
        
       
    
    def center(self):
        ww = self.winfo_reqwidth()
        hw = self.winfo_reqheight()

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x_pos = ws // 2 - ww // 2
        y_pos = hs // 2 - hw // 2

        self.place(x=x_pos, y=y_pos)

