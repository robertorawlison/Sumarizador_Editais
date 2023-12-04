# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import ImageTk

from entity import Document, TypeDocument
from .line_frame import LineFrame
        

DOC_COL = 0
CLASS_COL = 1

class ClassifierLineFrame(LineFrame):
    '''Widget personalizado para representar uma linha do catálogo de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, height : int, bg : str):
        self.height = height
        self.bg = bg
        num_cols = 2
        L = frame_master.winfo_reqwidth()# - 1 #Um pixel da coluna
        col_widths = [round(0.45 * L),
                      round(0.55 * L)]
        
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths)
        

class ClassifierDocumentFrame(ClassifierLineFrame):
    '''Widget personalizado para classificar o documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, doc : Document):
        super().__init__(frame_master, height=200, bg = "white")  #Cor do fundo da linha do DocumentFrame

        self.document = doc
        self.var_checkbox = tk.IntVar(value=1) #Variável de controle para saber se o checkbox está selecionado. Valor 1 indica que o mesmo começa marcado
        
    def is_checked(self) -> bool:
        #Retorna True indicando que o documento está marcado no checkbox
        if self.var_checkbox.get():
            return True
        else:
            return False
        
    def _open_file(self):
        self.document.open_file()
        
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
        
        #Checkbox
        checkbox = tk.Checkbutton(self.cell_frames[DOC_COL], bg=self.bg, var = self.var_checkbox)
        checkbox.pack(side="left", padx=60)
        
        frame_img = tk.Frame(self.cell_frames[DOC_COL], height=self.cell_frames[DOC_COL].winfo_reqheight(), bg = "white")
        frame_img.pack(pady=10, padx=10)
        
        #Image
        photo = ImageTk.PhotoImage(self.document.image)
        botao_img = tk.Button(frame_img, image=photo,  bg=self.bg, justify="center", command = self._open_file)
        botao_img.photo = photo
        botao_img.pack(side="top", pady=5)
        
        #Texto do tipo do documento
        l_type = tk.Label(frame_img, text=self.document.get_basename(), justify="center",  
                          wraplength=self.cell_frames[0].winfo_reqwidth(), bg = "white", 
                          font = tkFont.Font(family="Arial", size=14)
                          )
        l_type.pack(side="bottom")
        
        type_labels = [_type['label'] for _type in TypeDocument.list]
        self.combo = ttk.Combobox(self.cell_frames[CLASS_COL], values=type_labels, font=self.font, state="readonly")
        self.combo.set(self.document.type['label'])
        self.combo.pack(pady=75)
        self.combo.bind("<<ComboboxSelected>>", self.on_change)        

    def on_change(self, event):
        label = self.combo.get()
        self.document.type = TypeDocument.map[label]
        self.document.update_db_type()
        
        
        

class ClassifierHeaderFrame(ClassifierLineFrame):
    '''Widget personalizado para representar o cabeçalho do classificdor de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame):
        super().__init__(frame_master, height = 40, bg = "gray90")
        
    def _draw_cell(self, id_cell : int, text : str):
        label = tk.Label(self.cell_frames[id_cell], text=text, font=self.font, justify="center",  bg=self.bg)
        label.pack()
       
    def draw(self) -> None:
        super().draw()
        
        #Rótulos do cabeçalho
        texts = ["Doc.", "Classificação"]
        
        for _id, text in zip(range(len(texts)), texts):
            self._draw_cell(_id, text)
