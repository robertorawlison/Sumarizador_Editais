# -*- coding: utf-8 -*-
from .base_model import db
from .document_model import DocumentModel
from .document import Document

class Persistence:
    """
    Class responsável pela persistência das entidades do sistema
    """
    @classmethod
    def init(cls):
        db.connect()
        db.create_tables([DocumentModel])


    @classmethod
    def load_documents(cls):
        # Consultando e exibindo os registros na tabela
        docs_model = DocumentModel.select()
        if docs_model:
            documents = []
            for doc_model in docs_model:
                documents.append(Document(doc_db = doc_model))
            return documents
        else:
            return []
    
    @classmethod
    def finish(cls):
        db.close()
        

