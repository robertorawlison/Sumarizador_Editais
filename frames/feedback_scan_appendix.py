# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from .feedback_scan import FeedbackScan

class FeedbackScanAppendix(FeedbackScan):
    '''Widget personalizado para informar que a atividade está sendo processada durante o scan nos apensos
    '''
    def __init__(self, 
                 frame_master : tk.Frame, 
                 num_pages : int):
        
        super().__init__(frame_master)
        
        #Frame para as barras de progressão
        prog_bar_frame = tk.Frame(self, relief="ridge", borderwidth=5)
        prog_bar_frame.place(relx=0.5, rely=0.5, anchor="center")
        prog_bar_frame.lift()
        
        #Barra de proresso das páginas
        self.count_page = 0
        self.num_pages = num_pages
        
        
        self.l_count_pages = tk.Label(prog_bar_frame, font = ("Arial", 15),
                                    text = "Analisando página " + str(self.count_page) +" de " + str(self.num_pages))
        self.l_count_pages.pack(pady=1)
        
        self.l_active = tk.Label(prog_bar_frame, font = ("Arial", 15),
                                    text = "")
        self.l_active.pack(pady=1)
        
        self.prog_bar_page = ttk.Progressbar(prog_bar_frame, orient="horizontal", length=200, mode="determinate")
        self.prog_bar_page.pack(pady=5)
        
        self.prog_bar_page["value"] = 0
        self.step_pages = 100 / self.num_pages

        #Controle de documentos encontrados
        self.num_docs = 0
        self.l_scan = tk.Label(prog_bar_frame, font = ("Arial", 15),
                                    text = "0 documento encontrado.")
        self.l_scan.pack()
    
    def in_ocr(self):
         self.l_active.config(text="Lendo texto da página ...")
    
    def in_spellchecker(self):
         self.l_active.config(text="Checando ortografia e classificando o texto ...")
        
    def _update_count(self):
        self.prog_bar_page["value"] += self.step_pages
        self.count_page += 1
        self.l_count_pages.config(text="Tratando página " + str(self.count_page) +" de "+str(self.num_pages))
    
    def find_doc(self):
        self.num_docs += 1
        _text = f'{self.num_docs} documento encontrado.' if self.num_docs <= 1 else f'{self.num_docs} documentos encontrados.'
        self.l_scan.config(text=_text)
       