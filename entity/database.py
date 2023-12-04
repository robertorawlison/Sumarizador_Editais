# -*- coding: utf-8 -*-
from peewee import SqliteDatabase

class Database:
    """
    Class responsável pela persistência do sistema
    """
    db_name = 'database.db'
    db = SqliteDatabase(db_name)
    @classmethod
    def connect(cls):
        # Conectando ao banco de dados e criando a tabela
        Database.db.connect()

    @classmethod
    def close(cls):
        Database.db.close()