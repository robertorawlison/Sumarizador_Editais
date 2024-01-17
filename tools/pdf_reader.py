# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
import pytesseract, os
from PIL import Image, ImageEnhance, ImageFilter

from frames import FeedbackScan

pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'

os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR\tessdata'

#Configurações pro português
custom_config = r'--oem 3 --psm 6 -l por'


class PDFReader:
    ''' Classe que abstrai a leitura dos arquivos PDF.
        Primeira versão lê as páginas como sequencia de bytes
        Segunda versão lê as páginas como strings (arquivos nativos digitais)
        Terceira versão testa se o conteúdo é nativo digital ou imagem
    '''
    
    def __init__(self, file_name : str):
        self.file_name : str = file_name
        self.document : fitz.Document = fitz.open(self.file_name)
        self.fb = None
         
         
    def setFeedBack(self, fb : FeedbackScan) -> None:
        self.fb = fb
         
    def getNumPages(self) -> int:
        return self.document.page_count
    
    def getPageImage(self, num_page : int) -> Image: 
        #Captura a imagem da página num_page do pdf
        page = self.document[num_page]
        # Configurar a escala para 90x130 pixels
        escala_x = 90 / page.rect.width
        escala_y = 130 / page.rect.height

        # Configurar a matriz de transformação para ajustar a escala
        M = fitz.Matrix(escala_x, escala_y)
        pixmap = page.get_pixmap(matrix=M)
        return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    
    
    def splitFile(self, first_page : int, last_page : int) -> bytes:
        # Cria um novo documento PDF
        novo_pdf = fitz.open()
        novo_pdf.insert_pdf(self.document, from_page = first_page, to_page=last_page)
        novo_pdf.save('temp.pdf')
        novo_pdf.close()
        
         # Lê o conteúdo do arquivo como bytes
        with open('temp.pdf', "rb") as file:
           return file.read()
       
        #Remove o arquivo temporário
        os.remove('temp.pdf')
    
    def getPageText(self, num_page : int) -> str:
        page = self.document[num_page]
        return self._read_ocr_text(page)
    
    def close(self) -> None:
        self.document.close()
    
    def _read_ocr_text(self, page : fitz.Page) -> str:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if(self.fb):
            self.fb.update_image(img)
        largura, altura = img.size
        new_width = largura * 2  # Ajuste conforme necessário
        new_height = altura * 2
        img = img.resize((new_width, new_height), Image.BICUBIC)
        
        enhancer = ImageEnhance.Contrast(img)
        image = enhancer.enhance(2)  # Ajuste de contraste
        image = image.convert('L')  # Converter para escala de cinza
        image = image.filter(ImageFilter.SHARPEN)  # Aplicar nitidez
        return pytesseract.image_to_string(image, config=custom_config)