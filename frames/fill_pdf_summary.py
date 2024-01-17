# -*- coding: utf-8 -*-

import os
from entity import Document
from parsers import Parser
import tempfile
from datetime import datetime
from tools import PDFReader
from frames import FeedbackScanDocs

def fill_summary_from_pdf(doc : Document, fd : FeedbackScanDocs) -> (str, datetime):
    '''
    Extrai texto de um documento em PDF apontado pelo obejto doc e ativa o parser apropriado 
    para resumir seu conteúdo e acessar a data do documento.
    Se o texto do documento já foi extraído, a função apenas resume seu conteúdo.

    Parameters
    ----------
    doc : Document
        Objeto contendo os metadados de um documento pericial que está sendo tratado.
    fd : FeedbackScanDocs
        Atualiza a interface de retorno ao usuário sobre o que está sendo tratado atualmente no documento doc.

    Returns
    -------
    (str, datetime)
        Retorna uma tupla conteúdo uma string com resumo do texto e um objeto datetime contendo a data 
        do documento doc.

    '''
    if(doc.text == None):
        text = ""
        # Criar um arquivo temporário para armazenar os bytes do PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix=".pdf")
        # Escrever os bytes do PDF no arquivo temporário
        temp_pdf.write(doc.file_bytes)
        temp_pdf.close()
            
        # Abrir o PDF usando fitz
        pdf_document = PDFReader(temp_pdf.name)
        pdf_document.setFeedBack(fd)
        
        #Captura o número de páginas
        fd.reset_count_pages(pdf_document.getNumPages())
    
        for page_num in range(pdf_document.getNumPages()):
            text += pdf_document.getPageText(page_num)
            
        #Remove documento temporário
        pdf_document.close()
        os.remove(temp_pdf.name)
        doc.text = text #Coloca o texto extraído do pdf no objeto Document
        
    #Resumindo o texto lido do pdf
    fd.in_summary()
    
    summarizer = Parser.create_summarizer(doc)
    result = summarizer.summarize(doc.text)
    doc.summary = result[0]
    doc.date = result[1]
    


    
    
    





