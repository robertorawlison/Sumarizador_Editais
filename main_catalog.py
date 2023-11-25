# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog

from frames import FeedbackWindow, CatalogFrame, ClassifierFrame, PFFrame
from tools import print_word, fill_summary_numpages_from_pdf

import time
import threading
    

def click_report():
    if(cf != None):
        documents = cf.checked_documents()
        #Gerando a versão word do catálogo de documentos periciais
        print_word(documents)
            
               
def click_add():
    global cf, class_f, pff
        
    # Abre a janela de seleção de arquivos
    file_names = filedialog.askopenfilenames(
        initialdir="./",
        title="Selecione Arquivos",
        filetypes=(("Arquivos PDF", "*.pdf"),)
    )
    if file_names:
        if pff != None:
            pff.destroy()
            pff = None
        if(cf != None):
            cf.destroy()
            cf = None
        
        class_f = ClassifierFrame(root, width=1000)
        class_f.pack()
        
        class_f.create_documents(file_names)
        class_f.draw()
        
        botao_de_cat.configure(state="normal")
        botao_de_add.configure(state="disable")
        botao_de_rep.configure(state="disable")
   

def minha_thread(documents : list):
    global cf, class_f

    fw = FeedbackWindow(root, image_gear, len( documents))
    fw.center()
    
    #Pegando o sumário e o número de folhas de cada documento
    for doc in documents:
        #doc.create_summary_numpages(fw)
        fill_summary_numpages_from_pdf(doc, fw)
        
        time.sleep(3)
    
        cf.add([doc])
        fw.update_count_docs()
    
    fw.destroy()
    botao_de_rep.configure(state="normal")
    botao_de_add.configure(state="normal")
    

def click_catalog():
    global cf, class_f
    if class_f == None:
        return
    docs = class_f.checked_documents()
    class_f.destroy()
    class_f = None
    
    largura_tela = root.winfo_screenwidth()
    cf = CatalogFrame(root, width=largura_tela)
    cf.pack()
    cf.add([])
    
    th = threading.Thread(target=minha_thread, args=(docs,))
    th.start()

    botao_de_cat.configure(state="disable")
    


def on_enter_add(event):
    tooltip_add.place(in_=botao_de_add, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

def on_leave_add(event):
    tooltip_add.place_forget()

def on_enter_rep(event):
    tooltip_rep.place(in_=botao_de_rep, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

def on_leave_rep(event):
    tooltip_rep.place_forget()

def on_enter_cat(event):
    tooltip_cat.place(in_=botao_de_cat, anchor="c", bordermode="outside", relx=0.5, rely=1.1)

def on_leave_cat(event):
    tooltip_cat.place_forget()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sumarizador de documentos")
    root.iconbitmap("imagens/bot.ico")
    root.state("zoomed")  # Maximizar a janela sem cobrir a barra de tarefas
    
    # Carrega a imagem de fundo
    image_pf = tk.PhotoImage(file="imagens/pf-cinza.png")
    image_gear = tk.PhotoImage(file="imagens/gear.png")
    

    cf = None #CatalogFrame
    class_f = None #ClassifierFrame
    
    barra_horizontal = tk.Frame(root, height=5, bg="#0000FF")
    barra_horizontal.pack(fill="x")

    # Barra de Tarefas
    barra_de_tarefas = tk.Frame(root, bg="royal blue")
    barra_de_tarefas.pack(side="top", fill="x")
    
    
    botoes = tk.Frame(barra_de_tarefas, bg="royal blue")
    botoes.pack(anchor="center")

        
    # Botão para adição de novos documentos.
    img_add = tk.PhotoImage(file="imagens/add.png")
    botao_de_add = tk.Button(botoes, text="Adicionar documentos", image=img_add, command=click_add)
    botao_de_add.image = img_add
    botao_de_add.grid(row=0, column=0, pady=20, padx=10)
    
    # Associando os eventos ao botão
    botao_de_add.bind("<Enter>", on_enter_add)
    botao_de_add.bind("<Leave>", on_leave_add)
    
    tooltip_add = ttk.Label(root, text="Adicionar novos documentos periciais.", background="#FFFFE0", relief="solid")
    

    # Botão para geração de relatório no word.
    img_cat = tk.PhotoImage(file="imagens/catalog.png")
    botao_de_cat = tk.Button(botoes, text="Gerar catálogo de documentos periciais.", image=img_cat, command=click_catalog)
    botao_de_cat.image = img_cat
    botao_de_cat.grid(row=0, column=1, pady=20, padx=10)
    botao_de_cat.configure(state="disabled")
    
    # Associando os eventos ao botão
    botao_de_cat.bind("<Enter>", on_enter_cat)
    botao_de_cat.bind("<Leave>", on_leave_cat)
    
    tooltip_cat = ttk.Label(root, text="Gerar catálogo dos documentos periciais.", background="#FFFFE0", relief="solid")
    


    # Botão para geração de relatório no word.
    img_rep = tk.PhotoImage(file="imagens/word.png")
    botao_de_rep = tk.Button(botoes, text="Gerar relatório", image=img_rep, command=click_report)
    botao_de_rep.image = img_rep
    botao_de_rep.grid(row=0, column=2, pady=20, padx=10)
    botao_de_rep.configure(state="disabled")
    
    # Associando os eventos ao botão
    botao_de_rep.bind("<Enter>", on_enter_rep)
    botao_de_rep.bind("<Leave>", on_leave_rep)
    
    tooltip_rep = ttk.Label(root, text="Gerar relatório em word.", background="#FFFFE0", relief="solid")
    
    
    barra_horizontal = tk.Frame(root, height=5, bg="#0000FF")
    barra_horizontal.pack(fill="x")
    
    
    # Cria um widget Label com a imagem de fundo
    barra_de_tarefas.update_idletasks()
    shift_y = 2 * barra_horizontal.winfo_reqheight() + barra_de_tarefas.winfo_reqheight()
    pff = PFFrame(root, image_pf, shift_y)
    pff.pack()
    

    root.mainloop()