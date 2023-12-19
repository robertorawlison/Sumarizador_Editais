# -*- coding: utf-8 -*-
from PIL import Image
import io, subprocess, os
import fitz
from datetime import datetime

from .document_model import DocumentModel

class Document:
    '''Representa os dados dos documentos periciais avaliados
    '''
    def __init__(self, file_name:str = None, 
                 file_bytes:bytes = None, image:Image = None, 
                 num_pages:int = None, doc_db:DocumentModel = None):
        
        if(doc_db == None):
            self._file_name: str = file_name  # Nome do arquivo contendo o documento
            self._image : Image = image #Imagem na memória
            self._num_pages : int = 0  # Número de páginas
            self._file_bytes : bytes = file_bytes #Conteúdo em bytes do documento
            self._type : dict = TypeDocument.NON_CLASS #Tipo do documento
            self._summary : str = ""  # Resumo do documento
            self._date : datetime = None #Data de emissão do documento
            
            self._extract_file_metadata()
            # Criando instância da classe DocumentModel e inserindo no banco de dados
            self.db_instance = DocumentModel.create_db_instance(self) #Instância no database
            
            
        else:
            self._file_name = doc_db.file_name  
            self._image = Image.open(io.BytesIO(doc_db.image)) 
            self._type = TypeDocument().map[doc_db.type] 
            self._summary = doc_db.summary
            self._num_pages = doc_db.num_pages 
            self._date : datetime = doc_db.date
            self._file_bytes = doc_db.file_bytes 
            self.db_instance = doc_db
            
    def delete_db_instance(self):
        DocumentModel.delete_db_instance(self)
    
    def update_db_type(self):
        DocumentModel.update_type(self)
    
    def update_db_summary(self):
        DocumentModel.update_summary(self)
    
    def open_file(self):
        diretorio = os.path.dirname("temp/")

        # Verificar se o diretório existe, e criá-lo se não existir
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        file_name = os.path.basename(diretorio)+'/temp.pdf' 
        with open(file_name, 'wb') as pdf_file:
            pdf_file.write(self.file_bytes)
        
        subprocess.Popen(['start', "", file_name], shell=True)
    
    
    def to_string(self) -> str:
        str_doc = "Documento: " + self._file_name +"\n"
        str_doc += "Tipo: " + self._type['label'] + "\n"
        str_doc += "Descrição: " + self._summary + "\n"
        str_doc += "N. páginas: " + str(self._num_pages)
        return str_doc

    def _extract_file_metadata(self) -> None:
        # Lê o conteúdo do arquivo como bytes
        with open(self._file_name, "rb") as file:
           self._file_bytes = file.read()
        
        #Captura a imagem da primeira página do pdf
        pdf_file = fitz.open(self._file_name)
        self.num_pages = pdf_file.page_count
        
        # Configurar a escala para 90x130 pixels
        capa = pdf_file[0]
        escala_x = 90 / capa.rect.width
        escala_y = 130 / capa.rect.height

        # Configurar a matriz de transformação para ajustar a escala
        M = fitz.Matrix(escala_x, escala_y)
        pixmap = capa.get_pixmap(matrix=M)
        self.image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    
    def get_str_num_pages(self) -> str:
        #Texto do número de folhas
        num_p_str = str(self.num_pages)
        if(self.num_pages > 1):
            num_p_str += " fls."
        else:
            num_p_str += " fl."
        return num_p_str
    
    def get_str_date(self) -> str:
        if(self._date == datetime.max):
            return "desconhecido"
        else:
            return self._date.strftime("%d/%m/%Y")
    
    def get_basename(self):
        return os.path.basename(self.file_name)

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value : str):
        self._file_name = value

    @property
    def image_file(self) -> str:
        return self._image_file

    @image_file.setter
    def image_file(self, value : str):
        self._image_file = value

    @property
    def summary(self) -> str:
        return self._summary

    @summary.setter
    def summary(self, value : str):
        self._summary = value

    @property
    def num_pages(self) -> int:
        return self._num_pages

    @num_pages.setter
    def num_pages(self, value : int):
        self._num_pages = value
        
    @property
    def type(self) -> dict:
        return self._type

    @type.setter
    def type(self, value : dict):
        self._type = value
        
    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, value : Image):
        self._image = value

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value : datetime):
        self._date = value
        
    @property
    def file_bytes(self) -> bytes:
        return self._file_bytes

    @file_bytes.setter
    def file_bytes(self, value : bytes):
        self._file_byes = value


class TypeDocument:
    '''Tipos de documentos periciais'''
    NON_CLASS = {
        'label' : 'sem classificação',
        'plural' : 'sem classificação',
        'id' : 0
    }
    DESCONHECIDO = {
        'label' : 'desconhecido',
        'plural' : 'desconhecidos',
        'id' : 1
    }
    EDITAL = {
        'label' : 'edital',
        'plural' : 'editais',
        'id' : 2
    }
    CONTRATO  = {
        'label' : 'contrato',
        'plural' : 'contratos',
        'id' : 3
    }
    ADITIVO  = {
        'label' : 'aditivo',
        'plural' : 'aditivos',
        'id' : 4
    }
    PROCURACAO  = {
        'label' : 'procuração',
        'plural' : 'procurações',
        'id' : 5
    }
    list = [NON_CLASS, DESCONHECIDO, EDITAL, CONTRATO, ADITIVO, PROCURACAO]
    map = {f'{_type["label"]}' : _type for _type in list}