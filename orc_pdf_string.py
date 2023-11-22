# -*- coding: utf-8 -*-

import fitz  # PyMuPDF
import pytesseract
from PIL import Image

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'

# Função para extrair texto de uma página PDF usando pytesseract
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)

    return text

# Caminho do arquivo PDF
pdf_path = "docs/edital 1.pdf"

# Extrai texto do PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Imprime o texto final
print(pdf_text)

print("\n\n\n RESUMO: \n\n\n")



# Crie um analisador de texto
parser = PlaintextParser.from_string(pdf_text, Tokenizer("portuguese"))

# Escolha um método de sumarização (LSA neste exemplo)
summarizer = LuhnSummarizer()

# Obtém um resumo com 3 frases
resumo = summarizer(parser.document, 1)

# Imprime o resumo
for sentença in resumo:
    print(sentença)




