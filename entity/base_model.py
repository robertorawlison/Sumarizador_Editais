# -*- coding: utf-8 -*-
from peewee import Model, SqliteDatabase

db_name = 'database.db'
db = SqliteDatabase(db_name)

class BaseModel(Model):
    """
    Classe base para todos os Models usados no sistema.
    Define um database único
    """
    class Meta:
        database = db