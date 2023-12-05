# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

from entity import Forensic, TypeDocument

class ForensicFrame(tk.Frame):
    '''Widget personalizado para criar ou editar uma perícia na interface gráfica
    '''    
    def __init__(self, root : tk.Frame, width : int, forensic : Forensic):
        super().__init__(root, width=width, bg="white", highlightbackground="black", highlightthickness=1)  
        self.forensic = forensic
        
        self.font = tkFont.Font(family="Arial", size=20)
        
        
    def pack(self):
        super().pack(side="top")
        self.top_frame = tk.Frame(self, width=self.winfo_reqwidth(), bg="white")
        self.top_frame.pack(side="top")
        
        image_forensic = tk.PhotoImage(file="imagens/forensic2.png")
        self.label_forensic = tk.Label(self.top_frame, image=image_forensic, bg="white")
        self.label_forensic.image = image_forensic 
        self.label_forensic.pack(side="left")
        
        self.create_description()
        self.create_docs_counter()
        
    def create_description(self):    
        self.description_frame = tk.Frame(self.top_frame, bg="white")
        self.description_frame.pack(side="right")
        
        #Campo description
        label = tk.Label(self.description_frame, text="Descrição:", font=self.font, bg="white")
        label.grid(row=0, column=0, padx=5, pady=5)#, sticky="e")
        
        self.description_entry = tk.Entry(self.description_frame, font=self.font, highlightbackground="black", highlightthickness=1)
        self.description_entry.insert(0, self.forensic.description)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.description_entry.bind("<FocusOut>", self.on_description_entry_change)
        
        #Campo author
        label = tk.Label(self.description_frame, text="Perito:", font=self.font, bg="white")
        label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.author_entry = tk.Entry(self.description_frame, font=self.font, highlightbackground="black", highlightthickness=1)
        self.author_entry.insert(0, self.forensic.author)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.author_entry.bind("<FocusOut>", self.on_author_entry_change)
        
        #Campo date
        label = tk.Label(self.description_frame, text="Data-hora:", font=self.font, bg="white")
        label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        date_str = self.forensic.date.strftime("%d/%m/%Y - %H:%M")
        label = tk.Label(self.description_frame, 
                         text=date_str, justify="left", 
                         font=self.font, bg="white")
        label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        #Número de apensos
        num_docs = 0
        for a in self.forensic.appendices:
            num_docs += len(a.documents)
            
        label = tk.Label(self.description_frame, text="#Arquivos:", font=self.font, bg="white")
        label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        if(num_docs <= 1):
            text_appendices = f'{num_docs} documento'
        else:
            text_appendices = f'{num_docs} documentos'
        
        if(len(self.forensic.appendices) <= 1): 
            text_appendices += f' em {len(self.forensic.appendices)} apenso'
        else:
            text_appendices = f' em {len(self.forensic.appendices)} apensos'
        label = tk.Label(self.description_frame, 
                         text=text_appendices, 
                         justify="left", font=self.font, bg="white")
        label.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
    
    def on_description_entry_change(self, event):
        new_value = self.description_entry.get()
        if(self.forensic.description != new_value):
            self.forensic.description = new_value
            self.forensic.update_db_description()
            
    def on_author_entry_change(self, event):
        new_value = self.author_entry.get()
        if(self.forensic.author != new_value):
            self.forensic.author = new_value
            self.forensic.update_db_author()
        
        
    def create_docs_counter(self):
        #Contando quantos documentos de cada tipo
        counter = [0 for _ in range(len(TypeDocument.list))]
        for appendix in self.forensic.appendices:
            for doc in appendix.documents:
                counter[doc.type['id']] += 1
        
        if(sum(counter) == 0):
            return
        
        #Cria o frame do taskbar
        header_frame = tk.Frame(self, bg="grey70", highlightbackground="black", highlightthickness=1) 
        header_frame.pack(side="top", fill="x", pady=10)
        label = tk.Label(header_frame, text="Documentos classificados", font=self.font, bg="grey70")
        label.pack()
        
        self.counter_frame = tk.Frame(self, width=self.winfo_reqwidth(), bg="white")
        self.counter_frame.pack(side="bottom")
        
        self.update_idletasks()
        
        width = self.winfo_reqwidth() * 0.25
        r = c = 0 #Variável de controle do posicionamento dos frame de contagem no grid 
        for type_id in range(len(TypeDocument.list)):
            if counter[type_id] > 0:
                self.counter_doc_frame = tk.Frame(self.counter_frame, width=width, height=width/2, bg="white")
                self.counter_doc_frame.pack_propagate(False)
                self.counter_doc_frame.grid(row=r, column=c)
                
                num_font = tkFont.Font(family="Arial", size=24)
                if counter[type_id] < 10:
                    num_text = f'0{counter[type_id]}'
                else:
                    num_text = f'{counter[type_id]}'
                label = tk.Label(self.counter_doc_frame, text=num_text, font=num_font, bg="white")
                label.pack(anchor="center")
                
                type_font = tkFont.Font(family="Arial", size=18)
                if counter[type_id] == 1:
                    type_text = TypeDocument.list[type_id]['label']
                else:
                    type_text = TypeDocument.list[type_id]['plural']
                label = tk.Label(self.counter_doc_frame, text=type_text, font=type_font, bg="white")
                label.pack(anchor="center")
                
                
                #Cada linha possui apenas 4 colunas
                c = (c + 1) % 4 
                if(c == 0):
                    r += 1