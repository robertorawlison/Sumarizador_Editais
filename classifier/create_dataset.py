# -*- coding: utf-8 -*-


import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os, sys


pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR\tessdata'
#Configurações pro português
custom_config = r'--oem 3 --psm 6 -l por'


def create_text_dataset(file_name : str) -> str:
    pdf_document = fitz.open(file_name)
    
    #Coloca o texto da primeira página no diretório dataset/cover
    page = pdf_document[0]
    (_str, img) = page_to_string_image(page)
    print(f'Página 1 - Número de caracteres lidos: {len(_str)}')
    
    img.save("dataset/cover/cover.png", format='PNG')
    with open("dataset/cover/cover.txt", 'w') as arquivo:
        arquivo.write(_str)
    
    #Coloca as outras páginas no diretório dataset/non-cover 
    for page_num in range(1, pdf_document.page_count):
        page = pdf_document[page_num]
        (_str, img) = page_to_string_image(page)
        print(f'Página {(page_num+1)} - Número de caracteres lidos: {len(_str)}')
        
        img.save("dataset/non-cover/non-cover"+str(page_num)+".png", format='PNG')
        
        caminho_arquivo = "dataset/non-cover/non-cover"+str(page_num)+".txt"
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(_str)
        

def page_to_string_image(page) -> (str, Image):
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    largura, altura = img.size
    new_width = largura * 2  # Ajuste conforme necessário
    new_height = altura * 2
    img = img.resize((new_width, new_height),  Image.BICUBIC)
    enhancer = ImageEnhance.Contrast(img)
    image = enhancer.enhance(2)  # Ajuste de contraste
    image = image.convert('L')  # Converter para escala de cinza
    image = image.filter(ImageFilter.SHARPEN)  # Aplicar nitidez
    
    #Tesseract
    _str = pytesseract.image_to_string(image, config=custom_config)
    return (_str, img)


if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        for i in range(1, len(sys.argv)):
            file_name = sys.argv[i]
            print(f"Tratando arquivo: {file_name}")
            create_text_dataset(file_name)
    