# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog
import threading

from .feedback_window import FeedbackWindow 
from .catalog_frame import CatalogFrame 
from .classifier_frame import ClassifierFrame
from .pf_frame import PFFrame
from tools import print_word, fill_summary_numpages_from_pdf

class TaskManagerFrame(tk.Frame):
    '''Widget personalizado para representar a interface de gerenciamento das tarefas do sistema.
    '''
    def __init__(self, root : tk.Frame):
        self.master_frame = root
        self.cf : CatalogFrame = None #CatalogFrame
        self.class_f : ClassifierFrame = None #ClassifierFrame
        self.pff : PFFrame = None #PFFrame
        
        self.image_gear = tk.PhotoImage(file="imagens/gear.png")
        self.image_pf = tk.PhotoImage(file="imagens/pf-cinza.png")
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.master_frame, bg="royal blue") 
        super().pack(side="top", fill="x")
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        
    def pack(self):
        botoes = tk.Frame(self, bg="royal blue")
        botoes.pack(anchor="center")

        # Botão para adição de novos documentos.
        img_add = tk.PhotoImage(file="imagens/add.png")
        self.botao_de_add = tk.Button(botoes, text="Adicionar documentos", image=img_add, command=self.click_add)
        self.botao_de_add.image = img_add
        self.botao_de_add.grid(row=0, column=0, pady=20, padx=10)
        
        # Associando os eventos ao botão
        self.botao_de_add.bind("<Enter>", self.on_enter_add)
        self.botao_de_add.bind("<Leave>", self.on_leave_add)
        
        self.tooltip_add = ttk.Label(self.master_frame, text="Adicionar novos documentos periciais.", background="#FFFFE0", relief="solid")
        
        # Botão para geração de relatório no word.
        img_cat = tk.PhotoImage(file="imagens/catalog.png")
        self.botao_de_cat = tk.Button(botoes, text="Gerar catálogo de documentos periciais.", image=img_cat, command=self.click_catalog)
        self.botao_de_cat.image = img_cat
        self.botao_de_cat.grid(row=0, column=1, pady=20, padx=10)
        self.botao_de_cat.configure(state="disabled")
        
        # Associando os eventos ao botão
        self.botao_de_cat.bind("<Enter>", self.on_enter_cat)
        self.botao_de_cat.bind("<Leave>", self.on_leave_cat)
        
        self.tooltip_cat = ttk.Label(self.master_frame, text="Gerar catálogo dos documentos periciais.", background="#FFFFE0", relief="solid")
        
        # Botão para geração de relatório no word.
        img_rep = tk.PhotoImage(file="imagens/word.png")
        self.botao_de_rep = tk.Button(botoes, text="Gerar relatório", image=img_rep, command=self.click_report)
        self.botao_de_rep.image = img_rep
        self.botao_de_rep.grid(row=0, column=2, pady=20, padx=10)
        self.botao_de_rep.configure(state="disabled")
        
        # Associando os eventos ao botão
        self.botao_de_rep.bind("<Enter>", self.on_enter_rep)
        self.botao_de_rep.bind("<Leave>", self.on_leave_rep)
        
        self.tooltip_rep = ttk.Label(self.master_frame, text="Gerar relatório em word.", background="#FFFFE0", relief="solid")
        
        self.update_idletasks()
        
        shift_y = self.winfo_reqheight()
        self.pff = PFFrame(self.master_frame, self.image_pf, shift_y)
        self.pff.pack()
        
    def click_report(self):
        if(self.cf != None):
            documents = self.cf.checked_documents()
            #Gerando a versão word do catálogo de documentos periciais
            print_word(documents)
                
                   
    def click_add(self):
        # Abre a janela de seleção de arquivos
        file_names = filedialog.askopenfilenames(
            initialdir="./",
            title="Selecione Arquivos",
            filetypes=(("Arquivos PDF", "*.pdf"),)
        )
        if file_names:
            if self.pff != None:
                self.pff.destroy()
                self.pff = None
            if(self.cf != None):
                self.cf.destroy()
                self.cf = None
            
            self.class_f = ClassifierFrame(self.master_frame, width=700)
            self.class_f.pack()
            
            self.class_f.create_documents(file_names)
            self.class_f.draw()
            
            self.botao_de_cat.configure(state="normal")
            self.botao_de_add.configure(state="disable")
            self.botao_de_rep.configure(state="disable")
       

    def minha_thread(self, documents : list):
        fw = FeedbackWindow(self.master_frame, self.image_gear, len( documents))
        fw.center()
        
        #Pegando o sumário e o número de folhas de cada documento
        for doc in documents:
            fill_summary_numpages_from_pdf(doc, fw)
        
            self.cf.add(doc)
            fw.update_count_docs()
        
        fw.destroy()
        self.botao_de_rep.configure(state="normal")
        self.botao_de_add.configure(state="normal")
        

    def click_catalog(self):
        if self.class_f == None:
            return
        docs = self.class_f.checked_documents()
        self.class_f.destroy()
        self.class_f = None
        
        largura_tela = self.master_frame.winfo_screenwidth()
        self.cf = CatalogFrame(self.master_frame, width=largura_tela)
        self.cf.pack()
        
        th = threading.Thread(target=self.minha_thread, args=(docs,))
        th.start()

        self.botao_de_cat.configure(state="disable")
        

    def on_enter_add(self, event):
        self.tooltip_add.place(in_=self.botao_de_add, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

    def on_leave_add(self, event):
        self.tooltip_add.place_forget()

    def on_enter_rep(self, event):
        self.tooltip_rep.place(in_=self.botao_de_rep, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

    def on_leave_rep(self, event):
        self.tooltip_rep.place_forget()

    def on_enter_cat(self, event):
        self.tooltip_cat.place(in_=self.botao_de_cat, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

    def on_leave_cat(self, event):
        self.tooltip_cat.place_forget()
        