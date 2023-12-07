# -*- coding: utf-8 -*-
from peewee import CharField,  DateTimeField, ManyToManyField

from .base_model import BaseModel
from .appendix_model import AppendixModel

# Modelo para a tabela Document
class ForensicModel(BaseModel):
    """
    Modelo que representa a entidade Forensic no database
    """
    description = CharField()
    author = CharField()
    date = DateTimeField()
    
    appendices = ManyToManyField(AppendixModel, backref='forensic')
    
    @classmethod
    def create_db_instance(cls, forensic):
               
        # Criando instância da classe DocumentModel e inserindo no banco de dados
        db_instance = ForensicModel.create(
            description = forensic.description,
            author = forensic.author,
            date = forensic.date,
        )
        return db_instance
    
    @classmethod
    def delete_db_instance(cls, forensic):
        forensic.db_instance.delete_instance()
    
    @classmethod
    def update_description(cls, forensic):
        # Atualizando campo description
        print("Update")
        update = ForensicModel.update(description=forensic.description)
        update.where(ForensicModel.id == forensic.db_instance.id).execute()
        
    @classmethod
    def update_author(cls, forensic):
        # Atualizando campo author
        update = ForensicModel.update(author=forensic.author)
        update.where(ForensicModel.id == forensic.db_instance.id).execute()