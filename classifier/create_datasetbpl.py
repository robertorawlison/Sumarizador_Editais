# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:41:53 2023

@author: bruno.bpl
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR\tessdata'
# Configurações pro português
custom_config = r'--oem 3 --psm 6 -l por'


def processar_arquivo(file_name: str, output_directory: str) -> None:
    pdf_document = fitz.open(file_name)

    # Coloca o texto da primeira página no diretório dataset/cover
    page = pdf_document[0]
    (_str, img) = page_to_string_image(page)
    print(f'Página 1 - Número de caracteres lidos: {len(_str)}')

    img.save(os.path.join(output_directory, f'{os.path.basename(file_name).replace(".pdf", "_cover.png")}'), format='PNG')
    with open(os.path.join(output_directory, f'{os.path.basename(file_name).replace(".pdf", "_cover.txt")}'), 'w') as arquivo:
        arquivo.write(_str)

    # Coloca as outras páginas no diretório dataset/non-cover
    for page_num in range(1, pdf_document.page_count):
        page = pdf_document[page_num]
        (_str, img) = page_to_string_image(page)
        print(f'Página {(page_num+1)} - Número de caracteres lidos: {len(_str)}')

        img.save(os.path.join(output_directory, f'{os.path.basename(file_name).replace(".pdf", f"_non-cover{page_num}.png")}'), format='PNG')

        caminho_arquivo = os.path.join(output_directory, f'{os.path.basename(file_name).replace(".pdf", f"_non-cover{page_num}.txt")}')
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(_str)


def page_to_string_image(page) -> (str, Image):
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    largura, altura = img.size
    new_width = largura * 2  # Ajuste conforme necessário
    new_height = altura * 2
    img = img.resize((new_width, new_height), Image.BICUBIC)
    enhancer = ImageEnhance.Contrast(img)
    image = enhancer.enhance(2)  # Ajuste de contraste
    image = image.convert('L')  # Converter para escala de cinza
    image = image.filter(ImageFilter.SHARPEN)  # Aplicar nitidez

    # Tesseract
    _str = pytesseract.image_to_string(image, config=custom_config)
    return _str, img


def obter_diretorio():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    diretorio = filedialog.askdirectory(title="Selecione o diretório que contém os arquivos PDF")
    return diretorio


if __name__ == "__main__":
    diretorio = obter_diretorio()

    # Iterar sobre todos os arquivos no diretório
    for file_name in os.listdir(diretorio):
        if file_name.endswith(".pdf"):
            caminho_arquivo = os.path.join(diretorio, file_name)
            print(f"Tratando arquivo: {caminho_arquivo}")
            processar_arquivo(caminho_arquivo, diretorio)
