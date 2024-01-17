# -*- coding: utf-8 -*-
from peewee import CharField, IntegerField, DateTimeField, BlobField
import io
from .base_model import BaseModel

# Modelo para a tabela Document
class DocumentModel(BaseModel):
    """
    Modelo que repreenta a entidade Document no database
    """
    file_name = CharField()
    image = BlobField()
    type = CharField()
    file_bytes = BlobField()
    num_pages = IntegerField()
    first_page = IntegerField()
    last_page = IntegerField()
    
    summary = CharField(null=True)
    text = CharField(null=True)
    date = DateTimeField(null=True)

    @classmethod
    def create_db_instance(cls, doc):
        image_bytes = None
        with io.BytesIO() as byte_stream:
            doc.image.save(byte_stream, format="PNG")
            image_bytes = byte_stream.getvalue()
        
        # Criando instância da classe DocumentModel e inserindo no banco de dados
        db_instance = DocumentModel.create(
            file_name = doc.file_name,
            image = image_bytes,
            type = doc.type['label'],
            summary = doc.summary,
            text = doc.text,
            num_pages = doc.num_pages,
            first_page = doc.first_page,
            last_page = doc.last_page,
            date = doc.date,
            file_bytes = doc.file_bytes
        )
        return db_instance
    
    @classmethod
    def delete_db_instance(cls, doc):
        doc.db_instance.delete_instance()
    
    @classmethod
    def update_type(cls, doc):
        # Atualizando campo type. Sempre que o tipo do documento mudar seu sumário deve ser apagado.
        update = DocumentModel.update(type=doc.type['label'], summary = "")
        update.where(DocumentModel.id == doc.db_instance.id).execute()


    @classmethod
    def update_summary_date(cls, doc):
        # Atualizando campo summary, date
        if(doc.db_instance.text == None):
            update = DocumentModel.update(summary=doc.summary, date=doc.date, text=doc.text)
        else:
            update = DocumentModel.update(summary=doc.summary, date=doc.date)
        update.where(DocumentModel.id == doc.db_instance.id).execute()

    @classmethod
    def update_summary(cls, doc):
        # Atualizando campo summary
        update = DocumentModel.update(summary=doc.summary)
        update.where(DocumentModel.id == doc.db_instance.id).execute()

    @classmethod
    def update_date(cls, doc):
        # Atualizando campo summary, date
        update = DocumentModel.update(date=doc.date)
        update.where(DocumentModel.id == doc.db_instance.id).execute()
