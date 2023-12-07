# -*- coding: utf-8 -*-
from peewee import DoesNotExist

from .base_model import db
from .appendix_model import AppendixModel
from .document_model import DocumentModel
from .forensic_model import ForensicModel
from .forensic import Forensic

class Persistence:
    """
    Class responsável pela persistência das entidades do sistema
    """
    @classmethod
    def init(cls):
        db.connect()
        db.create_tables([DocumentModel, 
                          AppendixModel, 
                          AppendixModel.documents.get_through_model(),
                          ForensicModel,
                          ForensicModel.appendices.get_through_model()])

    @classmethod
    def listForensics(cls):
        forensics = []
        for forensic_db in ForensicModel.select():
            forensics.append(Forensic(forensic_db))
        return forensics
    
        
    @classmethod
    def finish(cls):
        db.close()
        

