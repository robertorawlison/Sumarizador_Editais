# -*- coding: utf-8 -*-
from peewee import CharField,  ManyToManyField

from .base_model import BaseModel
from .document_model import DocumentModel

# Modelo para a tabela Document
class AppendixModel(BaseModel):
    """
    Modelo que repreenta a entidade Appendix no database
    """
    name = CharField()
    documents = ManyToManyField(DocumentModel, backref='appendix')
    
    @classmethod
    def create_db_instance(cls, append):
               
        # Criando instância da classe DocumentModel e inserindo no banco de dados
        db_instance = AppendixModel.create(
            name = append.name
        )
        return db_instance