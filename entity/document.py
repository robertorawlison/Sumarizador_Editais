# -*- coding: utf-8 -*-
from PIL import Image
import os
import fitz
from datetime import datetime


class Document:
    '''Representa os dados dos documentos periciais avaliados
    '''
    def __init__(self, file_name : str):
        self._file_name: str = file_name  # Nome do arquivo contendo o documento
        self._image_file : str = None  # Nome do arquivo contendo a imagem da capa do documento
        self._image : Image = None #Imagem na memória
        self._type : dict = TypeDocument.DESCONHECIDO #Tipo do documento
        self._summary : str = ""  # Resumo do documento
        self._num_pages : int = 0  # Número de páginas
        self._date : datetime = None #Data de emissão do documento
        
    def to_string(self) -> str:
        str_doc = "Documento: " + self._file_name +"\n"
        str_doc += "Tipo: " + self._type['label'] + "\n"
        str_doc += "Descrição: " + self._summary + "\n"
        str_doc += "N. páginas: " + str(self._num_pages)
        return str_doc

    def create_image(self) -> None:
        #Captura a imagem da primeira página do pdf
        pdf_file = fitz.open(self._file_name)
        #M = fitz.Matrix(90, 130)
        capa = pdf_file[0]
        
        # Configurar a escala para 90x130 pixels
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


class TypeDocument:
    '''Tipos de documentos periciais'''
    DESCONHECIDO = {
        'label' : 'desconhecido',
        'plural' : 'desconhecidos',
        'id' : 0
    }
    EDITAL = {
        'label' : 'edital',
        'plural' : 'editais',
        'id' : 1
    }
    CONTRATO  = {
        'label' : 'contrato',
        'plural' : 'contratos',
        'id' : 2
    }
    ADITIVO  = {
        'label' : 'aditivo',
        'plural' : 'aditivos',
        'id' : 3
    }
    PROCURACAO  = {
        'label' : 'procuração',
        'plural' : 'procurações',
        'id' : 4
    }
    list = [EDITAL, CONTRATO, ADITIVO, PROCURACAO, DESCONHECIDO]
    map = {f'{_type["label"]}' : _type for _type in list}