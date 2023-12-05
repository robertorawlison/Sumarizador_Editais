# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import ImageTk

from entity import Forensic
from .line_frame import LineFrame
        

DOC_COL = 0
CLASS_COL = 1

class ForensicLineFrame(LineFrame):
    '''Widget personalizado para representar uma linha do catálogo de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, height : int, bg : str):
        self.height = height
        self.bg = bg
        num_cols = 1
        col_widths = frame_master.winfo_reqwidth()
        
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths)
        

class OpenForensicFrame(ForensicLineFrame):
    '''Widget personalizado para classificar o documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, forensic : Forensic):
        super().__init__(frame_master, height=200, bg = "white")  #Cor do fundo da linha do OpenForensicFrame

        self.forensic = forensic
        
    def _show_text_doc(self, event):
        # Função para exibir a janela com texto
        janela = tk.Toplevel(self.frame_summ)  # Cria uma nova janela
        janela.title("Informações do documento")  # Define o título da nova janela
    
        # Cria um widget de texto
        texto = tk.Text(janela, wrap=tk.WORD, font=tkFont.Font(family="Arial", size=18))
        texto.pack()
    
        # Adicione o texto que você deseja exibir
        texto.insert(tk.END, self.document.to_string())

       
    def draw(self) -> None:
        super().draw()
        
        frame_forensic = tk.Frame(self.cell_frames[0], height=self.cell_frames[0].winfo_reqheight(), bg = "white")
        frame_forensic.pack(pady=10, padx=10)
        
        #Image
        photo = tk.PhotoImage(file="imagens/forensic.png")
        botao_img = tk.Button(frame_forensic, image=photo,  bg=self.bg, justify="center", command = self._on_click)
        botao_img.photo = photo
        botao_img.pack(side="left", pady=5)
        
        #Texto do tipo do documento
        l_type = tk.Label(frame_forensic, text=self.forensic.to_string(), justify="center",  
                          wraplength=self.cell_frames[0].winfo_reqwidth(), bg = "white", 
                          font = tkFont.Font(family="Arial", size=18)
                          )
        l_type.pack(side="right")
        
            

    def on_click(self, event):
        self.forensic.load_appendices()