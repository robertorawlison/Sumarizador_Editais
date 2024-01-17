# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import TypeDocument

class BoardNumber(tk.Frame):
    APPENDIX = 0
    DOCUMENT = 1
    SUMMARY = 2
    NON_CLASSIFIE = 3
    TYPE_DOC = 4
    
    """
    Representa o número e sua descrição associada para um relatório de composição de elementos
    """

    def __init__(self, frame : tk.Frame,
                 number : int,  
                 type_board : int = TYPE_DOC, 
                 type_doc_id : int = -1, 
                 total_number : int = 0, 
                 font_color : str = "black", 
                 bg : str ="white", 
                 width : int = None, 
                 height : int = None):
        
        super().__init__(frame, bg = bg)
        self.type = type
        
        if width != None:
            self.configure(width = width)
        if height != None:
            self.configure(height = height)
            
            
        if type_board == BoardNumber.SUMMARY: #Se type == SUMMARY então deve indicar quantos doumentos faltam sumarizar (todos os documentos foram classificados)   
            if(number == 0):
                type_text = "sumarizado" if total_number == 1 else "sumarizados"
                number = total_number #Todos os documentos já foram classificados e sumarizados
            else:
                type_text = "não sumarizado" if number == 1 else "não sumarizados"
        elif type_board == BoardNumber.NON_CLASSIFIE: #Se type == NON_CLASSIF então falta documento ser classificado 
            type_text = "não classificado" if number == 1 else "não classificados"
        elif type_board == BoardNumber.APPENDIX: 
            type_text = "apenso" if number == 1 else "apensos"
        elif type_board == BoardNumber.DOCUMENT: 
            type_text = "documento" if number == 1 else "documentos"
        else:
            type_text = TypeDocument.list[type_doc_id]['label'] if number == 1 else TypeDocument.list[type_doc_id]['plural']
        
            
        
        num_text = f'0{number}' if number < 10 else f'{number}'
        total_num_text = f'0{total_number}' if total_number < 10 else f'{total_number}'
        
        if(number == total_number) and ((type_board == BoardNumber.TYPE_DOC) or (type_board == BoardNumber.APPENDIX) or (type_board == BoardNumber.DOCUMENT)): 
            num_text = total_num_text
        elif total_number > 0:
            num_text += f'/{total_num_text}'
        
        
        

        num_font = tkFont.Font(family="Arial", size=24)
        label = tk.Label(self, text=num_text, font=num_font, bg="white", fg=font_color)
        label.pack(anchor="center")
        
        type_font = tkFont.Font(family="Arial", size=18)
        label = tk.Label(self, text=type_text, font=type_font, bg="white", fg=font_color)
        label.pack(anchor="center")