# -*- coding: utf-8 -*-

import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os


from entity import Document
from parsers import Parser
from frames import FeedbackWindow
import tempfile

#from transformers import pipeline,  DistilBertTokenizer, DistilBertForQuestionAnswering


#import nltk
#nltk.download('punkt')

pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'

os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR\tessdata'

#Configurações pro português
custom_config = r'--oem 3 --psm 6 -l por'

# Função para extrair texto de uma página PDF usando pytesseract
def fill_summary_numpages_from_pdf(doc : Document, fd : FeedbackWindow) -> (str, int):
    #qa_pipeline = pipeline('question-answering', model='neuralmind/bert-base-portuguese-cased', tokenizer='neuralmind/bert-base-portuguese-cased')
    text = ""
    # Criar um arquivo temporário para armazenar os bytes do PDF
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix=".pdf")
    # Escrever os bytes do PDF no arquivo temporário
    temp_pdf.write(doc.file_bytes)
    temp_pdf.close()
        
    # Abrir o PDF usando fitz
    pdf_document = fitz.open(temp_pdf.name)
    
    #Captura o número de páginas
    fd.reset_count_pages(pdf_document.page_count)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        fd.update_image(img)
        largura, altura = img.size
        new_width = largura * 2  # Ajuste conforme necessário
        new_height = altura * 2
        img = img.resize((new_width, new_height), Image.BICUBIC)
        
        enhancer = ImageEnhance.Contrast(img)
        image = enhancer.enhance(2)  # Ajuste de contraste
        image = image.convert('L')  # Converter para escala de cinza
        image = image.filter(ImageFilter.SHARPEN)  # Aplicar nitidez
        text += pytesseract.image_to_string(image, config=custom_config)
        
    #Remove documento temporário
    pdf_document.close()
    os.remove(temp_pdf.name)
    #Resumindo o texto lido do pdf
    fd.in_summary()
    
    summarizer = Parser.create_summarizer(doc)
    result = summarizer.summarize(text)
    doc.summary = result[0]
    doc.date = result[1]
    
    





