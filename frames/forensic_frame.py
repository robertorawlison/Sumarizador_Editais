# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import Forensic, TypeDocument
from .board_number import BoardNumber
from .button import ClassifieButton, ReportButton, CatalogButton

class ForensicFrame(tk.Frame):
    '''Widget personalizado para criar ou editar uma perícia na interface gráfica
    '''    
    def __init__(self, root : tk.Frame, width : int, forensic : Forensic, task_manager):
        super().__init__(root, width=width, bg="white", 
                         highlightbackground="black", highlightthickness=1)  
        self.forensic = forensic
        self.task_manager = task_manager
        
        self.font = tkFont.Font(family="Arial", size=20)
        
        
    def pack(self):
        super().pack(side="top")
        self.top_frame = tk.Frame(self, width=self.winfo_reqwidth(), bg="white")
        self.top_frame.pack(side="top")
        
        image_forensic = tk.PhotoImage(file="imagens/forensic2.png")
        self.label_forensic = tk.Label(self.top_frame, image=image_forensic, bg="white")
        self.label_forensic.image = image_forensic 
        self.label_forensic.pack(side="left")
        
        self._count_documents()
        self._create_description()
        
        
        if(sum(self.counter) > 0):
            self._create_docs_report()
        
    def _create_description(self):    
        description_frame = tk.Frame(self.top_frame, bg="white")
        description_frame.pack(side="right")
        
        #Campo description
        label = tk.Label(description_frame, text="Descrição:", font=self.font, bg="white")
        label.grid(row=0, column=0, padx=5, pady=5)#, sticky="e")
        
        self.description_entry = tk.Entry(description_frame, font=self.font, highlightbackground="black", highlightthickness=1)
        self.description_entry.insert(0, self.forensic.description)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.description_entry.bind("<FocusOut>", self.on_description_entry_change)
        
        #Campo author
        label = tk.Label(description_frame, text="Perito:", font=self.font, bg="white")
        label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.author_entry = tk.Entry(description_frame, font=self.font, highlightbackground="black", highlightthickness=1)
        self.author_entry.insert(0, self.forensic.author)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.author_entry.bind("<FocusOut>", self.on_author_entry_change)
        
        #Campo date
        label = tk.Label(description_frame, text="Data-hora:", font=self.font, bg="white")
        label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        date_str = self.forensic.date.strftime("%d/%m/%Y - %H:%M")
        label = tk.Label(description_frame, 
                         text=date_str, justify="left", 
                         font=self.font, bg="white")
        label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self._docs_classification(description_frame)
        
        
    def _docs_classification(self, description_frame):
        ''' Indica a quantidade de documentos ainda não classificados.
            Se todos os documentos foram classificados então libera a geração de relatórios
            Se algum documento não estiver classificado libera a classificação de documentos'''
        label = tk.Label(description_frame, text="Status:", font=self.font, bg="white")
        label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        frame = tk.Frame(description_frame, bg="white")
        frame.grid(row=3, column=1, sticky="w")
        
        type_id = 0 # Id = 0 possui o contador de documentos não classificados
        total_docs = sum(self.counter)
        if(self.counter[type_id] > 0):
            bn = BoardNumber(frame = frame, 
                        number = self.counter[type_id],
                        total_number = total_docs,
                        type_doc_id = type_id,
                        font_color = "red")
                
        elif self.count_non_summary > 0 :
            bn = BoardNumber(frame = frame, 
                        number = self.count_non_summary,
                        total_number = total_docs,
                        type_doc_id = -1,
                        font_color = "red")
        else:
            bn = BoardNumber(frame = frame, 
                        number = total_docs,
                        total_number = total_docs,
                        type_doc_id = -1,
                        font_color = "blue")
        
        bn.pack(side='left', padx=10)
        
        
        if (self.counter[type_id] > 0) :
            button = ClassifieButton(frame, 
                                     on_click = self.task_manager.click_classifier)
        elif self.count_non_summary > 0 :
            button = CatalogButton(frame, 
                                   on_click = self.task_manager.click_catalog)    
        else:
            button = ReportButton(frame, 
                                  on_click = self.task_manager.click_report)
        
        button.pack(side='right', padx=12, pady=5)
         
        #catalog_button = CatalogButton(buttons_frame, self.task_manager.click_catalog)
        #catalog_button.grid(row=0, column=4, pady=10, padx=10)
        
        
    
    def on_description_entry_change(self, event):
        new_value = self.description_entry.get()
        if(self.forensic.description != new_value):
            self.forensic.description = new_value
            self.forensic.update_db_description()
            
    def on_author_entry_change(self, event):
        new_value = self.author_entry.get()
        if(self.forensic.author != new_value):
            self.forensic.author = new_value
            self.forensic.update_db_author()
        
    def _count_documents(self):
        #Contando quantos documentos classificados de cada tipo
        self.counter = [0 for _ in range(len(TypeDocument.list))]
        #Contando o número de documentos não sumarizados
        self.count_non_summary = 0;
        
        for appendix in self.forensic.appendices:
            for doc in appendix.documents:
                self.counter[doc.type['id']] += 1
                if doc.summary == "" :
                    self.count_non_summary += 1
        
        
    def _create_docs_report(self):
        #Cria o frame do taskbar
        header_frame = tk.Frame(self, bg="grey70", highlightbackground="black", highlightthickness=1) 
        header_frame.pack(side="top", fill="x", pady=10)
        label = tk.Label(header_frame, text="Documentos classificados", font=self.font, bg="grey70")
        label.pack()
        
        counter_frame = tk.Frame(self, width=self.winfo_reqwidth(), bg="white")
        counter_frame.pack(side="bottom")
        
        self.update_idletasks()
        
        width = self.winfo_reqwidth() * 0.25
        r = c = 0 #Variável de controle do posicionamento dos frame de contagem no grid 
        for type_id in range(1, len(TypeDocument.list)): #Igonora o primeiro que indica quem não foi classificado ainda
            if self.counter[type_id] > 0:
                bn = BoardNumber(frame = counter_frame,
                            width=width, 
                            height=width/2,
                            number = self.counter[type_id], 
                            type_doc_id = type_id)
                bn.pack_propagate(False)
                bn.grid(row=r, column=c)
                
                #Cada linha possui apenas 4 colunas
                c = (c + 1) % 4 
                if(c == 0):
                    r += 1