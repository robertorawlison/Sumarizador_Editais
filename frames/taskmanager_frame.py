# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import threading
from tools import print_word, fill_summary_numpages_from_pdf


from .feedback_window import FeedbackWindow 
from .catalog_frame import CatalogFrame 
from .classifier_frame import ClassifierFrame
from .pf_frame import PFFrame
from .forensic_frame import ForensicFrame
from .list_forensic_frame import ListForensicFrame
from .button import CreateButton, OpenButton, AddButton, CatalogButton, ReportButton
from entity import Forensic, Appendix, Persistence

class TaskManagerFrame(tk.Frame):
    '''Widget personalizado para representar a interface de gerenciamento das tarefas do sistema.
    '''
    def __init__(self, root : tk.Frame):
        self.master_frame = root
        self.cf : CatalogFrame = None 
        self.class_f : ClassifierFrame = None 
        self.pff : PFFrame = None 
        self.ff : ForensicFrame = None
        self.lff : ListForensicFrame = None
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        #Cria o frame para adicionar os DocumentFrames
        super().__init__(self.master_frame, height=100, bg="royal blue") 
        self.pack_propagate(False)
        super().pack(fill="x")
        
        barra_horizontal = tk.Frame(self.master_frame, height=5, bg="#0000FF")
        barra_horizontal.pack(fill="x")
        
        #Frames com os botões de ação
        self.current_task_frame = None
        self.buttons_frame = None
        
        #Persistência da perícia
        self.forensic = None
        Persistence.init()
        
        
    def pack(self):
        self.update_idletasks()
        open_frame = tk.Frame(self, bg="royal blue")
        open_frame.pack(side='left')
        
        
        create_button = CreateButton(open_frame, 0, self.click_create)
        create_button.pack()
        
        open_button = OpenButton(open_frame, 1, self.click_list)
        open_button.pack()
        
        self.update_idletasks()
        
        shift_y = self.winfo_reqheight()
        self.pff = PFFrame(self.master_frame, shift_y)
        self.pff.pack()
        
        
    def _create_buttons_frame(self):
        self.current_task_frame = tk.Frame(self, height=80, width=(self.winfo_screenwidth()*0.56), bg="grey70") 
        self.current_task_frame.pack_propagate(False)
        self.current_task_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_task_frame.configure(borderwidth=2, relief="solid")
    
        buttons_frame = tk.Frame(self.current_task_frame,  bg="grey70")
        buttons_frame.pack()
        
        
        self.num_label = tk.Label(buttons_frame, bg="grey70")
        self.num_label.grid(row=0, column=0)
        
        self.pipeline_label = tk.Label(buttons_frame, text="", bg="grey70", font=tkFont.Font(family="Arial", size=18))
        self.pipeline_label.grid(row=0, column=1)
        
        self.add_button = AddButton(buttons_frame, 2, self.click_add)
        self.add_button.pack()
        self.add_button.disactive()
        
        next_image = tk.PhotoImage(file="imagens/next.png")
        label_image = tk.Label(buttons_frame, image=next_image, bg="grey70")
        label_image.imagem = next_image
        label_image.grid(row=0, column=3)#, pady=10, padx=10)
        
        self.catalog_button = CatalogButton(buttons_frame, 4, self.click_catalog)
        self.catalog_button.pack()
        self.catalog_button.disactive()
        
        label_image = tk.Label(buttons_frame, image=next_image, bg="grey70")
        label_image.imagem = next_image
        label_image.grid(row=0, column=5)#, pady=10, padx=10)
        
        
        self.report_button = ReportButton(buttons_frame, 6, self.click_report)
        self.report_button.pack()
        self.report_button.disactive()
    
        
    def _forensic_buttons(self):
        num_image = tk.PhotoImage(file="imagens/um.png")
        self.num_label.configure(image = num_image)
        self.num_label.imagem = num_image
        
        self.pipeline_label.config(text="Cadastrando a perícia")
        self.add_button.active()
    
    def _classifier_buttons(self):
        num_image = tk.PhotoImage(file="imagens/dois.png")
        self.num_label.configure(image = num_image)
        self.num_label.imagem = num_image
        
        self.pipeline_label.config(text="Classificando documentos")
        self.add_button.disactive()
        self.catalog_button.active()
    
    def _catalog_buttons(self):
        num_image = tk.PhotoImage(file="imagens/tres.png")
        self.num_label.configure(image = num_image)
        self.num_label.imagem = num_image
        
        self.pipeline_label.config(text="Sumarizando documentos")
        self.catalog_button.disactive()
        self.report_button.active()
        
        
    def _clear_frames(self):
        if self.pff != None:
            self.pff.destroy()
            self.pff = None
        if(self.cf != None):
            self.cf.destroy()
            self.cf = None
        if(self.class_f != None):
            self.class_f.destroy()
            self.class_f = None
        if(self.ff != None):
            self.ff.destroy()
            self.ff = None
        if(self.lff != None):
            self.lff.destroy()
            self.lff = None
        
    
    def click_list(self):
        self._clear_frames()
        self.lff = ListForensicFrame(self.master_frame, 
                                     width = self.winfo_screenwidth()*0.46,
                                     command_open = self.open_forensic,
                                     command_del = self.click_list)
        self.lff.pack()
        
    
    def click_report(self):
        if(self.cf != None):
            documents = self.cf.checked_documents()
            #Gerando a versão word do catálogo de documentos periciais
            print_word(documents)
                
                   
    def click_create(self):
        self.forensic = None
        foren = Forensic()
        append = Appendix(name="apenso 1")
        foren.add(append)
        
            
        self.open_forensic(foren)
    
    
    def open_forensic(self, foren : Forensic):
        '''Tela de exibição dos dados de um Forensic. Esta função é chamada para abrir 
        uma nova perícia ou para abrir na tela de listagem das perícias do BD.'''
        self.forensic = foren
        self._clear_frames()
        self._create_buttons_frame()
        self._forensic_buttons()
        
        self.ff = ForensicFrame(self.master_frame, width=self.current_task_frame.winfo_reqwidth(), forensic = self.forensic)
        self.ff.pack()
        
        
                
    def click_add(self):
        #Abre a janela de seleção de arquivos
        file_names = filedialog.askopenfilenames(
            initialdir="./",
            title="Selecione Arquivos",
            filetypes=(("Arquivos PDF", "*.pdf"),)
        )
        if file_names:
            self._clear_frames()
            self._classifier_buttons()
            
            self.class_f = ClassifierFrame(self.master_frame,  width=self.current_task_frame.winfo_reqwidth(), forensic=self.forensic)
            self.class_f.pack()
            
            self.class_f.create_documents(file_names)
            self.class_f.draw()
            
            

    def minha_thread(self, documents : list):
        fw = FeedbackWindow(self.master_frame, len( documents))
        fw.center()
        
        #Pegando o sumário e o número de folhas de cada documento
        for doc in documents:
            if(doc.summary == ""): #Não sumarizou seu conteúdo
                fill_summary_numpages_from_pdf(doc, fw)
                doc.update_db_summary()
        
            self.cf.add(doc)
            fw.update_count_docs()
        
        fw.destroy()
        

    def click_catalog(self):
        if self.class_f == None:
            return
        docs = self.class_f.checked_documents()
        
        self._clear_frames()
        self._catalog_buttons()
        
        largura_tela = self.master_frame.winfo_screenwidth()
        self.cf = CatalogFrame(self.master_frame, width=largura_tela)
        self.cf.pack()
        
        th = threading.Thread(target=self.minha_thread, args=(docs,))
        th.start()