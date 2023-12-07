# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import Forensic, Persistence
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
        col_widths = [frame_master.winfo_reqwidth()]
        
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths)
        

class OpenForensicFrame(ForensicLineFrame):
    '''Widget personalizado para classificar o documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, forensic : Forensic, command_open, command_del):
        super().__init__(frame_master, height=90, bg = "white")  #Cor do fundo da linha do OpenForensicFrame

        self.forensic = forensic
        self.command_open = command_open
        self.command_del = command_del
        
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
        
        frame_forensic = tk.Frame(self.cell_frames[0],  height=self.cell_frames[0].winfo_reqheight(), bg = "white")
        frame_forensic.pack(side='left')
        
        frame_button = tk.Frame(frame_forensic, bg = "white")
        frame_button.pack(side="left", padx=20)
        
        #Image
        photo = tk.PhotoImage(file="imagens/open_forensic.png")
        button_open = tk.Button(frame_button, image=photo,  bg=self.bg, justify="left", command = self._on_click_open)
        button_open.photo = photo
        button_open.pack(padx=10,pady=5)
        
        photo = tk.PhotoImage(file="imagens/delete.png")
        button_del = tk.Button(frame_button, image=photo,  bg=self.bg, justify="left", command = self._on_click_delete)
        button_del.photo = photo
        button_del.pack(padx=10,pady=5)
        
        #Texto do tipo do documento
        l_type = tk.Label(frame_forensic, text=self.forensic.to_string(), justify="left",  
                          wraplength=self.cell_frames[0].winfo_reqwidth(), bg = "white", 
                          font = tkFont.Font(family="Arial", size=18)
                          )
        l_type.pack(side="right")
        
            

    def _on_click_open(self):
        self.forensic.load_appendices()
        self.command_open(self.forensic)
        
    def _on_click_delete(self):
        self.forensic.delete_db_instance()
        self.command_del()