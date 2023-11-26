# -*- coding: utf-8 -*-
"""
Instanciador do resumidor específico. O objeto Document define o tipo de summarizador
"""
from entity import Document

from .unknown import UnknownSummarizer
from .edital import EditalSummarizer
from .contrato import ContratoSummarizer


class Parser:
    @classmethod
    def create_summarizer(cls, doc : Document):
        if doc.type == Document.DESCONHECIDO :
            return UnknownSummarizer()
        elif doc.type == Document.EDITAL :
            return EditalSummarizer()
        elif doc.type == Document.CONTRATO :
            return ContratoSummarizer()