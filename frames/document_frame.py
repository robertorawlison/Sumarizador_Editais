# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
import math
from PIL import ImageTk 

from entity import Document, Persistence
from .line_frame import LineFrame       

IMG_COL = 0
TYPE_COL = 1
SUMM_COL = 2
DATE_COL = 3
NUMP_COL = 4

class CatalogLineFrame(LineFrame):
    '''Widget personalizado para representar uma linha do catálogo de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, height, bg : str):
        self.height = height
        self.bg = bg
        
        L = frame_master.winfo_reqwidth()
        num_cols = 5
        col_widths = [math.floor(0.1 * L),
                      math.floor(0.1 * L),
                      math.floor(0.6 * L),
                      math.floor(0.1 * L),
                      math.floor(0.1 * L)]
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths)
        

class DocumentFrame(CatalogLineFrame):
    '''Widget personalizado para representar os dados do documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, doc : Document, command_del):
        super().__init__(frame_master, height=150, bg = "white")  #Cor do fundo da linha do DocumentFrame

        self.document = doc
        self.var_checkbox = tk.IntVar(value=1) #Variável de controle para saber se o checkbox está selecionado. Valor 1 indica que o mesmo começa marcado
        self.command_del = command_del
        
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
        janela = tk.Toplevel(self.cell_frames[SUMM_COL])  # Cria uma nova janela
        janela.title("Informações do documento")  # Define o título da nova janela
    
        # Cria um widget de texto
        texto = tk.Text(janela, wrap=tk.WORD, font=tkFont.Font(family="Arial", size=18))
        texto.pack()
    
        # Adicione o texto que você deseja exibir
        texto.insert(tk.END, self.document.to_string())
        
    def _on_click_delete(self):
        Persistence.delete_doc(self.document)
        self.command_del(self.document)

       
    def draw(self) -> None:
        super().draw()
        #Checkbox e delete button
        frame = tk.Frame(self.cell_frames[IMG_COL], bg=self.bg, highlightbackground="grey80", highlightthickness=1)
        frame.pack(padx=10, side="left")
        
        checkbox = tk.Checkbutton(frame, bg=self.bg, var = self.var_checkbox)
        checkbox.pack(pady=5)
        
        photo = tk.PhotoImage(file="imagens/delete2.png")
        button_del = tk.Button(frame, image=photo,  bg=self.bg, 
                               command = self._on_click_delete)
        button_del.photo = photo
        button_del.pack(pady=5)
        
        
        #Image
        photo = ImageTk.PhotoImage(self.document.image)
        botao_img = tk.Button(self.cell_frames[IMG_COL], image=photo,  bg=self.bg, justify="center", command = self._open_file)
        botao_img.photo = photo
        botao_img.pack(padx=5, pady=3)
        
        #Texto do tipo do documento
        l_type = tk.Label(self.cell_frames[TYPE_COL], text=self.document.type['label'], font=self.font, justify="center",  
                          wraplength=self.cell_frames[TYPE_COL].winfo_reqwidth(), bg=self.bg)
        l_type.pack(pady=50)
        
        #Texto da descrição do documento
        text_label = tk.Label(self.cell_frames[SUMM_COL], text=self.document.summary, font=self.font, justify="left", 
                              wraplength=self.cell_frames[SUMM_COL].winfo_reqwidth(), bg=self.bg)
        text_label.pack()
        #Exibe o texto em uma janela ao clickar no frame ou no rótulo
        self.cell_frames[SUMM_COL].bind("<Button-1>", self._show_text_doc)
        text_label.bind("<Button-1>", self._show_text_doc)
        
        #Texto da data do documento
        date = tk.Label(self.cell_frames[DATE_COL], text=self.document.get_str_date(), 
                        font=self.font, justify="center",  bg=self.bg)
        date.pack(pady=60)
        
        #Texto do número de folhas
        numero = tk.Label(self.cell_frames[NUMP_COL], text=self.document.get_str_num_pages(), 
                          font=self.font, justify="center",  bg=self.bg)
        numero.pack(pady=60)
        
        

class HeaderFrame(CatalogLineFrame):
    '''Widget personalizado para representar o cabeçalho do catálogo de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame):
        super().__init__(frame_master, height = 40, bg = "gray90")
        
    def _draw_cell(self, id_cell : int, text : str):
        font = tkFont.Font(family="Arial", size=18)
        label = tk.Label(self.cell_frames[id_cell], text=text, font=font, justify="center",  bg=self.bg)
        label.pack()
       
    def draw(self) -> None:
        super().draw()
        
        #Rótulos do cabeçalho
        texts = ["Doc.", "Tipo", "Descrição", "Data", "# folhas"]
        
        for _id, text in zip(range(len(texts)), texts):
            self._draw_cell(_id, text)
        


