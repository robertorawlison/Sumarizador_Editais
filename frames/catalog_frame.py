# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from sortedcontainers import SortedList

from .document_frame import DocumentFrame, HeaderFrame
from entity import Document

class CatalogFrame(tk.Frame):
    '''Widget personalizado para um catálogo de documentos periciais na interface gráfica
    '''    
    def __init__(self, root : tk.Frame, width : int, command_del):
        # Frame com barra de rolagem      
        self.frame_master = tk.Frame(root, width=width)
        self.scrollbar = ttk.Scrollbar(self.frame_master, orient="vertical")
        self.command_del = command_del
        
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
        self.documents = SortedList(key=lambda doc: doc.date) #Documentos periciais ordenados por sua data de emissão 
      
        
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
        
    def _clear_doc_frames(self):
        for docf in self.doc_frames:
            docf.destroy()
        self.doc_frames = []
        
    def add(self, documents : list) -> None:
        '''Desenha uma tabela contendo o catálogo de documentos periciais analisados (CatologFrame).
        ''Para cada objeto Document cria uma linha através do DocumentFrame a ser desenhado no CatologFrame
        '''
        self._clear_doc_frames()
        
        #self.canvas.delete("all")
        
        #Ordena a lista de documentos pela data de emissão do documento
        for document in documents:
            self.documents.add(document)
            
        for doc in self.documents:
            df = DocumentFrame(self, doc, self.command_del)
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
