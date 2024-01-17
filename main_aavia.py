# -*- coding: utf-8 -*-
import tkinter as tk
from frames import TaskManagerFrame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Assistente de análise de viabilidade")
    root.iconbitmap("imagens/bot.ico")
    root.state("zoomed")  # Maximizar a janela sem cobrir a barra de tarefas
    
    taskbar = TaskManagerFrame(root)
    taskbar.pack()

    root.mainloop() 