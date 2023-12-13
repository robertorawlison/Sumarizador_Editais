# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

class LineFrame(tk.Frame):
    '''Widget personalizado para criar linhas de tabelas contendo widgets iterativos (botões, marcadores e etc) em suas células.
    '''    
    def __init__(self, frame_master : tk.Frame, _height : int, _bg : str, num_col : int, col_widths : list, propagate : bool = False):
        super().__init__(frame_master, width=frame_master.winfo_reqwidth(), height=_height, bg=_bg)
        self.pack_propagate(propagate)
        self.pack()
        
        self.cell_frames = [None] * num_col
        self.col_widths = col_widths
        
        #Fonte dos textos contidos na linha
        self.font = tkFont.Font(family="Arial", size=14)
    
        
    def draw(self) -> None:
        for i in range(len(self.cell_frames)):
            self.cell_frames[i] = tk.Frame(self, height=self.height, 
                                           width=self.col_widths[i], 
                                           bg=self.bg)
            self.cell_frames[i].pack_propagate(False)
            self.cell_frames[i].grid(row=0, column=i)
            self.cell_frames[i].configure(borderwidth=1, relief="solid")
            
