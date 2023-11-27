# -*- coding: utf-8 -*-


import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os, sys, time


pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR\tessdata'
#Configurações pro português
custom_config = r'--oem 3 --psm 6 -l por'


def read_text(file_name : str) -> str:    
    text = ""
    pdf_document = fitz.open(file_name)
    #Captura o número de páginas
   
    tt = 0
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        largura, altura = img.size
        new_width = largura * 2  # Ajuste conforme necessário
        new_height = altura * 2
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        enhancer = ImageEnhance.Contrast(img)
        image = enhancer.enhance(2)  # Ajuste de contraste
        image = image.convert('L')  # Converter para escala de cinza
        image = image.filter(ImageFilter.SHARPEN)  # Aplicar nitidez
        
        #Tesseract
        ti = time.time()
        _str = pytesseract.image_to_string(image, config=custom_config)
        tf = time.time()
        
        text += _str
        td = tf - ti
        tt += td
        print(f'Página {(page_num+1)} - Número de caracteres lidos: {len(_str)} - ORC tempo: {td:.2f} s')
     
    print(f'Tempo total: {tt:.2f} s')
    return text


if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        for i in range(1, len(sys.argv)):
            file_name = sys.argv[i]
            print(f"Tratando arquivo: {file_name}")
            text = read_text(file_name)
            print(f'Número total de caracteres lidos {len(text)} \n')
    else:
        print("Linha de comando: python test_tesseract <lista de nome dos pdfs teste>")