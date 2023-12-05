# -*- coding: utf-8 -*-
from peewee import DoesNotExist

from .base_model import db
from .appendix_model import AppendixModel
from .document_model import DocumentModel
from .forensic_model import ForensicModel
from .forensic import Forensic
from .appendix import Appendix

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
    def load_forensic(cls):
         forensic_description = "Perícia policial"
         try:
             forensic_db = ForensicModel.select().where(ForensicModel.description == forensic_description).get()
             return Forensic(forensic_db = forensic_db)
         except DoesNotExist:
             forensic = Forensic()
             
             append = Appendix(name="apenso 1")
             forensic.add(append)
             
             return forensic

        
    @classmethod
    def finish(cls):
        db.close()
        

