# -*- coding: utf-8 -*-
"""
Classe apenso, para representar um conjunto de documentos periciais
"""

class Appendix:
    def __init__(self):
        self._documents = [] #Lista de documentos periciais


    # Métodos get e set para os campos da classe
    @property
    def documents(self) -> list:
        return self._documents
    
    @documents.setter
    def documents(self, value: list) -> None:
        self._documents = value
