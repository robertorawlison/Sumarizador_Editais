# -*- coding: utf-8 -*-
"""
Class que representa uma perícia documental realizada por um perito
"""
from datetime import datetime

from .forensic_model import ForensicModel
from .appendix import Appendix

class Forensic:
    def __init__(self, forensic_db:ForensicModel = None):
        if(forensic_db == None):
            self._appendices: list = []  # Lista de apensos
            self._description: str = "Perícia policial"  # Descrição da perícia
            self._author: str = "nome do perito"  # Identificação do perito autor da perícia
            self._date: datetime = datetime.now()  # Data e hora de criação da perícia
            self.db_instance = ForensicModel.create_db_instance(self) #Instância no database
        else:
            self._description = forensic_db.description
            self._author = forensic_db.author
            self._date = forensic_db.date
            self.db_instance = forensic_db
            
            self._appendices = []
    
    def to_string(self) -> str:
        str_forensic = "Descrição: " + self._description + "\n"
        str_forensic += "Autor: " + self._author + "\n"
        str_forensic += "Data de criação: " + self._date.strftime("%d/%m/%Y")
        return str_forensic
    
                
    def load_appendices(self):
        for append_db in self.db_instance.appendices:
            self._appendices.append(Appendix(append_db = append_db))
            
    def add(self, append : Appendix):
        self._appendices.append(append)
        self.db_instance.appendices.add([append.db_instance])
        self.db_instance.save()
        
        
    def update_db_description(self):
        ForensicModel.update_description(self)
    
    def update_db_author(self):
        ForensicModel.update_author(self)
    

    # Métodos get e set para os campos da classe
    @property
    def appendices(self) -> list:
        return self._appendices

    @appendices.setter
    def appendices(self, value: list) -> None:
        self._appendices = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        self._author = value

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: datetime) -> None:
        self._date = value

