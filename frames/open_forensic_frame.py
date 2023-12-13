# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import Forensic, Persistence
from .line_frame import LineFrame
from.board_number import BoardNumber
        
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
        
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths, True)
        

class OpenForensicFrame(ForensicLineFrame):
    '''Widget personalizado para classificar o documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, forensic : Forensic, command_open, command_del):
        super().__init__(frame_master, height=120, bg = "white")  #Cor do fundo da linha do OpenForensicFrame

        self.forensic = forensic
        self.command_open = command_open
        self.command_del = command_del
        
       
    def draw(self) -> None:
        super().draw()
        
        frame_forensic = tk.Frame(self.cell_frames[0],  
                                  height=self.cell_frames[0].winfo_reqheight(), bg = "white")
        frame_forensic.pack(side='left')
        
        frame_button = tk.Frame(frame_forensic, bg = "white")
        frame_button.grid(row=0, column=0, padx=20, sticky="w")
        
        #Image
        photo = tk.PhotoImage(file="imagens/open_forensic.png")
        button_open = tk.Button(frame_button, image=photo,  bg=self.bg, justify="left", 
                                command = self._on_click_open)
        button_open.photo = photo
        button_open.pack(padx=10, pady=5)
        
        photo = tk.PhotoImage(file="imagens/delete.png")
        button_del = tk.Button(frame_button, image=photo,  bg=self.bg, justify="left", 
                               command = self._on_click_delete)
        button_del.photo = photo
        button_del.pack(padx=10, pady=5)
        
        #Texto sobre a perícia
        l_type = tk.Label(frame_forensic, text=self.forensic.to_string(), justify="left",  
                          #wraplength=self.cell_frames[0].winfo_reqwidth(),
                          bg = "white", 
                          font = tkFont.Font(family="Arial", size=20)
                          )
        l_type.grid(row=0, column=1)

        
        #Contabilizando o número de apensos e documentos no BD associados a esta perícia
        num_appendices = len(self.forensic.db_instance.appendices)
        num_docs = 0
        for append_db in self.forensic.db_instance.appendices:
            num_docs += len(append_db.documents)

        frame = tk.Frame(frame_forensic, bg = "white", highlightbackground="grey80", highlightthickness=1)
        frame.grid(row=0, column=2, padx=30)

        bn = BoardNumber(frame = frame, 
                     number = num_appendices,
                     type_board = BoardNumber.APPENDIX)
        bn.pack(side='left', padx=5)
        
        
        bn = BoardNumber(frame = frame, 
                     number = num_docs,
                     type_board = BoardNumber.DOCUMENT)
        bn.pack(side='right', padx=5)
        
            
    def _on_click_open(self):
        self.forensic.load_appendices()
        self.command_open(self.forensic)
        
    def _on_click_delete(self):
        Persistence.delete(self.forensic)
        self.command_del()