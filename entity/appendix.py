# -*- coding: utf-8 -*-

from .document import Document
from .appendix_model import AppendixModel
from .document_model import DocumentModel

class Appendix:
    """
    Classe apenso, para representar um conjunto de documentos periciais
    """
    def __init__(self, name:str = None, append_db:AppendixModel = None):
        if(append_db == None):
            self._name = name #Nome identificador do apenso
            self._documents = [] #Lista de documentos periciais
            self.db_instance = AppendixModel.create_db_instance(self) #Instância no database
        else:
            self._name = append_db.name
            self.db_instance = append_db
            self._documents = []
            for doc_db in self.db_instance.documents.order_by(DocumentModel.date):
                self._documents.append(Document(doc_db = doc_db))

    def add(self, doc : Document):
        self._documents.append(doc)
        self.db_instance.documents.add([doc.db_instance])
        self.db_instance.save()
        
    def delete_db_instance(self):
        for doc in self.documents:
            print("del doc")
            doc.delete_db_instance()
        AppendixModel.delete_db_instance(self)


    # Métodos get e set para os campos da classe
    @property
    def documents(self) -> list:
        return self._documents
    
    @documents.setter
    def documents(self, value: list) -> None:
        self._documents = value
        
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
