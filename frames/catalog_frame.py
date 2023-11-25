# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from .document_frame import DocumentFrame, HeaderFrame

class CatalogFrame(tk.Frame):
    '''Widget personalizado para um catálogo de documentos periciais na interface gráfica
    '''    
    def __init__(self, root : tk.Frame, width : int):
        # Frame com barra de rolagem      
        self.frame_master = tk.Frame(root, width=width)
        self.scrollbar = ttk.Scrollbar(self.frame_master, orient="vertical")
        
        diff = self.frame_master.winfo_reqwidth()-self.scrollbar.winfo_reqwidth()
        self.canvas = tk.Canvas(self.frame_master, width=diff)
        self.canvas.pack_propagate(False)
        
        #Captura eventos de atualização no scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self._on_configure)
        
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.canvas, width=diff, bg="white", highlightbackground="black", highlightthickness=1)  
        self.doc_frames = [] #Frames dos documentos periciais
      
        
    def pack(self):
        self.frame_master.pack(fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="y", expand=True)
        self.canvas.create_window((0, 0), window=self, anchor="nw")
        
        
        
        #desenhando o cabeçalho
        hf = HeaderFrame(self)
        hf.draw()
        hf.update_idletasks()
        
        
    def destroy(self):
        self.pack_forget()
        super().destroy()
        self.frame_master.pack_forget()
        self.frame_master.destroy()
        
        
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def add(self, documents : list) -> None:
        '''Desenha uma tabela contendo o catálogo de documentos periciais analisados (CatologFrame).
        ''Para cada objeto Document cria uma linha através do DocumentFrame a ser desenhado no CatologFrame
        '''
        #self.canvas.delete("all")
        for doc in documents:
            df = DocumentFrame(self, doc)
            df.draw()
            self.doc_frames.append(df)
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
            
    def checked_documents(self) -> list:
        '''Retorna os objetos Document que foram marcados em sua interface
        '''
        documents = []
        for df in self.doc_frames:
            if df.is_checked():
                documents.append(df.document)
            
        return documents
