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
    
    summary = CharField(null=True)
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
            num_pages = doc.num_pages,
            date = doc.date,
            file_bytes = doc.file_bytes
        )
        return db_instance
    
    @classmethod
    def update_type(cls, doc):
        # Atualizando campo type
        update = DocumentModel.update(type=doc.type['label'])
        update.where(DocumentModel.id == doc.db_instance.id).execute()


    @classmethod
    def update_summary(cls, doc):
        # Atualizando campo summary, date
        update = DocumentModel.update(summary=doc.summary, date=doc.date)
        update.where(DocumentModel.id == doc.db_instance.id).execute()
