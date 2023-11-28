# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog
import threading
from tools import print_word, fill_summary_numpages_from_pdf


from .feedback_window import FeedbackWindow 
from .catalog_frame import CatalogFrame 
from .classifier_frame import ClassifierFrame
from .pf_frame import PFFrame
from .button import AddButton, CatalogButton, ReportButton 

class TaskManagerFrame(tk.Frame):
    '''Widget personalizado para representar a interface de gerenciamento das tarefas do sistema.
    '''
    def __init__(self, root : tk.Frame):
        self.master_frame = root
        self.cf : CatalogFrame = None #CatalogFrame
        self.class_f : ClassifierFrame = None #ClassifierFrame
        self.pff : PFFrame = None #PFFrame
        
        self.image_gear = tk.PhotoImage(file="imagens/gear.png")
        self.image_pf = tk.PhotoImage(file="imagens/pf-cinza.png")
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.master_frame, bg="royal blue") 
        super().pack(side="top", fill="x")
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        
    def pack(self):
        botoes_frame = tk.Frame(self, bg="royal blue")
        botoes_frame.pack(anchor="center")
        
        self.add_button = AddButton(botoes_frame, self.click_add)
        self.add_button.pack()
        
        self.catalog_button = CatalogButton(botoes_frame, self.click_catalog)
        self.catalog_button.pack()
        self.catalog_button.disactive()
        
        self.report_button = ReportButton(botoes_frame, self.click_report)
        self.report_button.pack()
        self.report_button.disactive()
        
        self.update_idletasks()
        
        shift_y = self.winfo_reqheight()
        self.pff = PFFrame(self.master_frame, self.image_pf, shift_y)
        self.pff.pack()
        
    def click_report(self):
        if(self.cf != None):
            documents = self.cf.checked_documents()
            #Gerando a versão word do catálogo de documentos periciais
            print_word(documents)
                
                   
    def click_add(self):
        # Abre a janela de seleção de arquivos
        file_names = filedialog.askopenfilenames(
            initialdir="./",
            title="Selecione Arquivos",
            filetypes=(("Arquivos PDF", "*.pdf"),)
        )
        if file_names:
            if self.pff != None:
                self.pff.destroy()
                self.pff = None
            if(self.cf != None):
                self.cf.destroy()
                self.cf = None
            
            self.class_f = ClassifierFrame(self.master_frame, width=700)
            self.class_f.pack()
            
            self.class_f.create_documents(file_names)
            self.class_f.draw()
            
            self.catalog_button.active()
            self.add_button.disactive()
            self.report_button.disactive()
            

    def minha_thread(self, documents : list):
        fw = FeedbackWindow(self.master_frame, self.image_gear, len( documents))
        fw.center()
        
        #Pegando o sumário e o número de folhas de cada documento
        for doc in documents:
            fill_summary_numpages_from_pdf(doc, fw)
        
            self.cf.add(doc)
            fw.update_count_docs()
        
        fw.destroy()
        self.report_button.active()
        self.add_button.active()
        

    def click_catalog(self):
        if self.class_f == None:
            return
        docs = self.class_f.checked_documents()
        self.class_f.destroy()
        self.class_f = None
        
        largura_tela = self.master_frame.winfo_screenwidth()
        self.cf = CatalogFrame(self.master_frame, width=largura_tela)
        self.cf.pack()
        
        th = threading.Thread(target=self.minha_thread, args=(docs,))
        th.start()

        self.catalog_button.disactive() 