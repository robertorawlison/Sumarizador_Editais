# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from classifier_document_frame import ClassifierDocumentFrame, ClassifierHeaderFrame
from document import Document

class ClassifierFrame(tk.Frame):
    '''Widget personalizado para a interface de classificação de documentos periciais na interface gráfica
    '''    
    def __init__(self, root : tk.Frame, width : int):
        # Frame com barra de rolagem      
        self.frame_master = tk.Frame(root, height=650, width=width)
        self.scrollbar = ttk.Scrollbar(self.frame_master, orient="vertical")
        
        diff = self.frame_master.winfo_reqwidth()-self.scrollbar.winfo_reqwidth()
        self.canvas = tk.Canvas(self.frame_master, width=diff, height=self.frame_master.winfo_reqheight())
        
        #Captura eventos de atualização no scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self._on_configure)
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.canvas, height=self.frame_master.winfo_reqheight(), width=diff, bg="white", highlightthickness=1, highlightbackground="black")  
  
        self.class_doc_frames = [] #Frames dos documentos periciais
      
        
    def pack(self):
        self.frame_master.pack(expand=True)
        self.scrollbar.pack(side="right", fill="y",)
        self.canvas.pack(side="left", fill="y", expand=True)
        self.canvas.create_window((0, 0), window=self, anchor="nw")
        
       
    def destroy(self):
        self.frame_master.pack_forget()
        
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def create_documents(self, file_names : list):
        self.documents = []
        
        for file in file_names:
            doc = Document(file)
            doc.create_image()
            self.documents.append(doc)
        
        
    def draw(self):
        '''Desenha uma tabela contendo os documentos periciais analisados (CatologFrame).
        ''Para cada objeto Document cria uma linha através do DocumentFrame a ser desenhado no CatologFrame
        '''
        
        chf = ClassifierHeaderFrame(self)
        chf.draw()
        
        for doc in self.documents:
            cdf = ClassifierDocumentFrame(self, doc)
            cdf.draw()
            self.class_doc_frames.append(cdf)
            
    def checked_documents(self) -> list:
        '''Retorna os objetos Document que foram marcados em sua interface
        '''
        documents = []
        for cdf in self.class_doc_frames:
            if cdf.is_checked():
                cdf.document.type = cdf.combo.get()
                documents.append(cdf.document)
            
        return documents
