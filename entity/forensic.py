# -*- coding: utf-8 -*-
"""
Class que representa uma perícia documental realizada por um perito
"""
from datetime import datetime

class Forensic:
    def __init__(self):
        self._appendices: list = []  # Lista de apensos
        self._description: str = ""  # Descrição da perícia
        self._author: str = ""  # Identificação do perito autor da perícia
        self._date: datetime = datetime.now()  # Data e hora de criação da perícia

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

