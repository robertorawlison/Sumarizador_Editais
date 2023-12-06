# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from .open_forensic_frame import OpenForensicFrame
from entity import Forensic, Persistence

class ListForensicFrame(tk.Frame):
    '''Widget personalizado para a interface de listagem das perícias cadastradas.
    '''    
    def __init__(self, root : tk.Frame, width : int, command_open, command_del):
        # Frame com barra de rolagem      
        self.frame_master = tk.Frame(root, height=550, width=width)
        self.scrollbar = ttk.Scrollbar(self.frame_master, orient="vertical")
        
        diff = self.frame_master.winfo_reqwidth()-self.scrollbar.winfo_reqwidth()
        self.canvas = tk.Canvas(self.frame_master, width=diff, height=self.frame_master.winfo_reqheight())
        
        #Captura eventos de atualização no scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self._on_configure)
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.canvas, height=self.frame_master.winfo_reqheight(), width=diff, bg="white", highlightthickness=1, highlightbackground="black")  
  
        self.open_forensic_frames = [] #Frames dos documentos periciais
        self.command_open = command_open
        self.command_del = command_del
        
    def pack(self) -> None:
        self.frame_master.pack(expand=True)
        self.scrollbar.pack(side="right", fill="y",)
        self.canvas.pack(side="left", fill="y", expand=True)
        self.canvas.create_window((0, 0), window=self, anchor="nw")
        
        self.draw()
        
       
    def destroy(self) -> None:
        self.frame_master.pack_forget()
        
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
    def draw(self) -> None:
        '''Desenha uma lista de periciais analisadas 
        ''Para cada objeto Document cria uma linha através do DocumentFrame a ser desenhado no CatologFrame
        '''
        for forensic in Persistence.listForensics():
            off = OpenForensicFrame(self, forensic, self.command_open, self.command_del)
            off.draw()
            self.open_forensic_frames.append(off)
            
    

