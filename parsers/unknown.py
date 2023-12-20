# -*- coding: utf-8 -*-
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

from .summarizer import Summarizer
from datetime import datetime

class UnknownSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        # Crie um analisador de texto
        parser = PlaintextParser.from_string(text, Tokenizer("portuguese"))
    
        # Escolha um método de sumarização (LSA neste exemplo)
        summarizer = LuhnSummarizer()
    
        summary = str(summarizer(parser.document, 1)[0]) # Obtém um resumo com 1 frase
        date = Summarizer._encontra_data(self, text)
        return (summary, date)
