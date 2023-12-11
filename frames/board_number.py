# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import TypeDocument

class BoardNumber(tk.Frame):
    """
    Representa o número e sua descrição associada para um relatório de composição de elementos
    """

    def __init__(self, frame : tk.Frame, number : int,  type_doc_id : int, 
                 total_number : int = 0, font_color : str = "black", 
                 bg : str ="white", width : int = None, height : int = None):
        
        super().__init__(frame, bg = bg)
        if width != None:
            self.configure(width = width)
        if height != None:
            self.configure(height = height)
        
        num_font = tkFont.Font(family="Arial", size=24)
        num_text = f'0{number}' if number < 10 else f'{number}'
        total_num_text = f'0{total_number}' if total_number < 10 else f'{total_number}'
        
        if(number == 0):
            num_text = total_num_text
        elif total_number > 0:
            num_text += f'/{total_num_text}'
            
        label = tk.Label(self, text=num_text, font=num_font, bg="white", fg=font_color)
        label.pack(anchor="center")
        
        type_font = tkFont.Font(family="Arial", size=18)
        if(number == 0):
            type_text = "classificados"
        elif number == 1:
            type_text = TypeDocument.list[type_doc_id]['label']
        else:
            type_text = TypeDocument.list[type_doc_id]['plural']
        label = tk.Label(self, text=type_text, font=type_font, bg="white", fg=font_color)
        label.pack(anchor="center")