# -*- coding: utf-8 -*-
from peewee import DoesNotExist

from .base_model import db
from .appendix_model import AppendixModel
from .document_model import DocumentModel
from .forensic_model import ForensicModel
from .forensic import Forensic
from .document import Document

class Persistence:
    """
    Class responsável pela persistência das entidades do sistema
    """
    @classmethod
    def init(cls) -> None:
        db.connect()
        db.create_tables([DocumentModel, 
                          AppendixModel, 
                          AppendixModel.documents.get_through_model(),
                          ForensicModel,
                          ForensicModel.appendices.get_through_model()])

    @classmethod
    def listForensics(cls) -> None:
        forensics = []
        for forensic_db in ForensicModel.select():
            forensics.append(Forensic(forensic_db))
        return forensics
    
    @classmethod
    def delete(cls, forensic : Forensic) -> None:
        for append_db in forensic.db_instance.appendices:
            for doc_db in append_db.documents:
                append_db.documents.remove(doc_db)
            forensic.db_instance.appendices.remove(append_db)
        forensic.db_instance.delete_instance()
 
    
    @classmethod
    def delete_doc(cls, document : Document) -> None:
        '''
        Remove a instância Document_model associada ao objeto document, removendo também a relação com 
        o objeto da classe Appendix
        '''
        append = document.db_instance.appendix[0] #Cada Document se relaciona com um único Appendix
        append.documents.remove(document.db_instance)
        document.db_instance.delete_instance()
        
        
    @classmethod
    def finish(cls):
        db.close()
        

