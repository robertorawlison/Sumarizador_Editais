# -*- coding: utf-8 -*-

from budget_PDF_reader import BudgetPDFReader
from budget_XLSX_writer import BudgetXLSXWriter


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

def selecionar_arquivo():
    # Abre a janela de seleção de arquivo
    arquivo = filedialog.askopenfilename(initialdir="./", title="Selecione um arquivo", filetypes=(("Arquivos PDF", "*.pdf"),))

    try:
        # Exibe o nome do arquivo selecionado
        if arquivo:
            label_gear = tk.Label(janela, image=imagem_gear)
            label_gear.place(x=0, y=0, relwidth=1, relheight=1)
            janela.update()
            
            print("Arquivo selecionado:", arquivo)
            pdf = BudgetPDFReader(arquivo)
            budget = pdf.read()
            budget.compute_metrics()
            output_file = arquivo.split(".")[0] + ".xlsx"
            xlsx = BudgetXLSXWriter(output_file)
            xlsx.write(budget)
            
            label_gear.destroy()
            messagebox.showinfo("Sucesso!", "Orçamento convertido para planilha: " + output_file)
    except PermissionError:
        label_gear.destroy()
        messagebox.showerror("Erro!", "Não há permissão para escrever no arquivo: " + output_file)
    #except:
    #    label_gear.destroy()
    #    messagebox.showerror("Erro!", "Orçamento não foi convertido.")


# Cria a janela principal
janela = tk.Tk()
janela.title("Converter")
janela.iconbitmap("imagens/bot.ico")
janela.state("zoomed")

# Carrega a imagem de fundo
imagem_fundo = ImageTk.PhotoImage(Image.open("imagens/pf.png"))

# Cria um widget Label com a imagem de fundo
label_fundo = tk.Label(janela, image=imagem_fundo)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Cria um botão para selecionar o arquivo 
imagem_botao = ImageTk.PhotoImage(Image.open("imagens/pdfTOxlsx.png"))
botao_selecionar = tk.Button(janela, image=imagem_botao, command=selecionar_arquivo)
botao_selecionar.pack()

botao_selecionar.place(x=100, y=100)

img = Image.open("imagens/gear.png")
imagem_gear = ImageTk.PhotoImage(img)

# Inicia o loop principal da janela
janela.mainloop()


