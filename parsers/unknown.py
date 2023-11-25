# -*- coding: utf-8 -*-
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

from .summarizer import Summarizer

class UnknownSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        # Crie um analisador de texto
        parser = PlaintextParser.from_string(text, Tokenizer("portuguese"))
    
        # Escolha um método de sumarização (LSA neste exemplo)
        summarizer = LuhnSummarizer()
    
    
        # Obtém um resumo com 1 frase
        return str(summarizer(parser.document, 1)[0])

