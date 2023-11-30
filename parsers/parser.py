# -*- coding: utf-8 -*-
"""
Instanciador do resumidor específico. O objeto Document define o tipo de summarizador
"""
from entity import Document, TypeDocument

from .unknown import UnknownSummarizer
from .edital import EditalSummarizer
from .contrato import ContratoSummarizer


class Parser:
    @classmethod
    def create_summarizer(cls, doc : Document):
        if doc.type['id'] == TypeDocument.EDITAL['id'] :
            return EditalSummarizer()
        elif doc.type['id'] == TypeDocument.CONTRATO['id'] :
            return ContratoSummarizer()
        else:
            return UnknownSummarizer()
        