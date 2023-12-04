# -*- coding: utf-8 -*-
from peewee import DoesNotExist

from .base_model import db
from .appendix_model import AppendixModel
from .document_model import DocumentModel
from .appendix import Appendix

class Persistence:
    """
    Class responsável pela persistência das entidades do sistema
    """
    @classmethod
    def init(cls):
        db.connect()
        db.create_tables([DocumentModel, AppendixModel, AppendixModel.documents.get_through_model()])


    @classmethod
    def load_appendix(cls):
        append_name = "apenso 1"
        try:
            appendix_db = AppendixModel.select().where(AppendixModel.name == append_name).get()
            return Appendix(append_db = appendix_db)
        except DoesNotExist:
            return Appendix(name = append_name)

        
    @classmethod
    def finish(cls):
        db.close()
        

