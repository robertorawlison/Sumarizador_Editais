# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
import math
from PIL import ImageTk 
from datetime import datetime
from tkcalendar import Calendar

from entity import Document, Persistence
from .line_frame import LineFrame       

IMG_COL = 0
TYPE_COL = 1
SUMM_COL = 2
DATE_COL = 3
APPEND_COL = 4
NUMP_COL = 5

class CatalogLineFrame(LineFrame):
    '''Widget personalizado para representar uma linha do catálogo de documentos periciais na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, height, bg : str):
        self.height = height
        self.bg = bg
        
        L = frame_master.winfo_reqwidth()
        num_cols = 6
        col_widths = [math.floor(0.09 * L),
                      math.floor(0.08 * L),
                      math.floor(0.58 * L),
                      math.floor(0.1 * L),
                      math.floor(0.07 * L),
                      math.floor(0.08 * L)]
        super().__init__(frame_master, self.height, self.bg, num_cols, col_widths)

class DocumentFrame(CatalogLineFrame):
    '''Widget personalizado para representar os dados do documento pericial na interface gráfica
    '''
    def __init__(self, frame_master : tk.Frame, doc : Document, command_del):
        super().__init__(frame_master, height=150, bg = "white")  #Cor do fundo da linha do DocumentFrame

        self.document = doc
        self.var_checkbox = tk.IntVar(value=1) #Variável de controle para saber se o checkbox está selecionado. Valor 1 indica que o mesmo começa marcado
        self.command_del = command_del
        
        #Widgets de exibição/edição do summary
        self.text_label = None
        self.text_entry = None
        self.button_edit = None
        self.button_not_edit = None
        
        
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
        
    def _change_date(self):
        date = datetime.strptime(self.calendar.get_date(), "%m/%d/%y")
        print(f"Data selecionada: {date}")
        if(date != self.document.date):    
            #Atualizando a data no documento
            self.document.date = date
            self.document.update_db_date()
            self.date_label.configure(text=self.document.get_str_date())
        
        self.window_cal.destroy()  # Fecha a janela após capturar a data
        self.window_cal = None
        self.calendar = None


    def _on_click_calendar(self):
        self.window_cal = tk.Toplevel(self.cell_frames[DATE_COL])
        self.window_cal.iconbitmap("imagens/bot.ico")
        self.window_cal.title("Nova data")
        #self.window_cal.overrideredirect(True)  # Remove a barra de título
       
        #Centralizando o calendário relativo ao frame da data
        diff_x = self.window_cal.winfo_reqwidth() - self.cell_frames[DATE_COL].winfo_reqwidth()
        diff_y = self.window_cal.winfo_reqheight() - self.cell_frames[DATE_COL].winfo_reqheight()
        x_pos = self.cell_frames[DATE_COL].winfo_rootx() - diff_x // 2
        y_pos = self.cell_frames[DATE_COL].winfo_rooty() - diff_y // 2
        self.window_cal.geometry(f"+{x_pos}+{y_pos}")


        # Configura o calendário com a data atual
        if(self.document.date == datetime.max):
            date = datetime.now()
        else:
            date = self.document.date
        self.calendar = Calendar(self.window_cal, selectmode="day", year=date.year, month=date.month, day=date.day)
        self.calendar.pack(pady=20)

        botao_obter_data = tk.Button(self.window_cal, text="salvar", command=self._change_date)
        botao_obter_data.pack(pady=10)
        
    def _draw_summary_text(self):
        '''Exibe o texto de descrição do documento.'''
        if(self.text_entry != None):
           self.text_entry.destroy()
           self.text_entry = None
           self.button_not_edit.destroy()
           self.button_not_edit = None
       
        self.cell_frames[SUMM_COL].configure(highlightbackground="black", highlightthickness=1, borderwidth=1)
        
        self.text_label = tk.Label(self.cell_frames[SUMM_COL], text=self.document.summary, font=self.font, justify="left", 
                              wraplength=self.cell_frames[SUMM_COL].winfo_reqwidth(), bg=self.bg)
        self.text_label.pack()
        
        photo = ImageTk.PhotoImage(file="imagens/edit.png")
        self.button_edit = tk.Button(self.cell_frames[SUMM_COL], image=photo,  bg=self.bg, justify="center", command = self._draw_summary_edit_text)
        self.button_edit.photo = photo
        
        #Posicionando o botao no canto inferior direito
        pos_x = self.cell_frames[SUMM_COL].winfo_reqwidth() - self.button_edit.winfo_reqwidth() - 5
        pos_y = self.cell_frames[SUMM_COL].winfo_reqheight() - self.button_edit.winfo_reqheight() - 5
        self.button_edit.place(x=pos_x, y=pos_y)
        
        #Exibe o texto em uma janela ao clickar no frame ou no rótulo
        self.text_label.bind("<Button-1>", self._show_text_doc)
    
    def _edit_summary_text(self):
        text = self.text_entry.get("1.0", tk.END)
        if(text != self.document.summary):
            self.document.summary = text
            self.document.update_db_summary()
            
        self._draw_summary_text()
    
    def _draw_summary_edit_text(self):
        '''Exibe o texto de descrição do documento.'''
        if(self.text_label != None):
           self.text_label.destroy()
           self.text_label = None
           self.button_edit.destroy()
           self.button_edit = None
           
        self.cell_frames[SUMM_COL].configure(highlightbackground="blue", highlightthickness=1, borderwidth=5)
        self.text_entry = tk.Text(self.cell_frames[SUMM_COL],  
                                   width=self.cell_frames[SUMM_COL].winfo_reqwidth(),
                                   height=self.cell_frames[SUMM_COL].winfo_reqheight(),
                                   wrap="word",
                                   font=self.font, 
                                   bg=self.bg)
        
        self.text_entry.insert("1.0", self.document.summary)
        self.text_entry.pack()
        
        photo = ImageTk.PhotoImage(file="imagens/not-edit.png")
        self.button_not_edit = tk.Button(self.cell_frames[SUMM_COL], image=photo,  bg=self.bg, justify="center", command = self._edit_summary_text)
        self.button_not_edit.photo = photo
        
        #Posicionando o botao no canto inferior direito
        pos_x = self.cell_frames[SUMM_COL].winfo_reqwidth() - self.button_not_edit.winfo_reqwidth() - 5
        pos_y = self.cell_frames[SUMM_COL].winfo_reqheight() - self.button_not_edit.winfo_reqheight() - 5
        self.button_not_edit.place(x=pos_x, y=pos_y)
        
        
       
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
        button_img = tk.Button(self.cell_frames[IMG_COL], image=photo,  bg=self.bg, justify="center", command = self._open_file)
        button_img.photo = photo
        button_img.pack(padx=5, pady=3)
        
        #Texto do tipo do documento
        l_type = tk.Label(self.cell_frames[TYPE_COL], 
                          text=self.document.type['label'], 
                          font=self.font, 
                          justify="center",  
                          wraplength=self.cell_frames[TYPE_COL].winfo_reqwidth(), 
                          bg=self.bg)
        l_type.pack(pady=50)
        
        #Texto da descrição do documento
        self._draw_summary_text()
        self.cell_frames[SUMM_COL].bind("<Button-1>", self._show_text_doc)
        
        #Texto da data do documento
        frame = tk.Frame(self.cell_frames[DATE_COL], 
                         bg=self.bg, 
                         highlightbackground="grey80", 
                         highlightthickness=1)
        frame.pack(pady=40)
        
        
        self.date_label = tk.Label(frame, 
                                   text=self.document.get_str_date(), 
                                   font=self.font, 
                                   justify="center",  
                                   bg=self.bg)
        self.date_label.pack()
        
        photo = ImageTk.PhotoImage(file="imagens/calendar.png")
        botao_cal = tk.Button(frame, image=photo,  bg=self.bg, justify="center", command = self._on_click_calendar)
        botao_cal.photo = photo
        botao_cal.pack(padx=5)
        
        
        #Texto do nome do apenso
        apenso = tk.Label(self.cell_frames[APPEND_COL], 
                          text=self.document.appendix.name, 
                          wraplength=self.cell_frames[APPEND_COL].winfo_reqwidth(),
                          font=self.font, 
                          justify="center",  
                          bg=self.bg)
        apenso.pack(pady=60)
        
        #Texto do número de folhas
        numero = tk.Label(self.cell_frames[NUMP_COL], 
                          text=self.document.get_str_num_pages(), 
                          wraplength=self.cell_frames[NUMP_COL].winfo_reqwidth(),
                          font=self.font, 
                          justify="center",  
                          bg=self.bg)
        numero.pack(pady=40)
        
        

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
        texts = ["Doc.", "Tipo", "Descrição", "Data", "Arquivo", "# folhas"]
        
        for _id, text in zip(range(len(texts)), texts):
            self._draw_cell(_id, text)
        


