# -*- coding: utf-8 -*-
import re
from datetime import datetime
from .summarizer import Summarizer

class ContratoSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        partes = self._encontra_partes(text)
        objeto = self._encontra_objeto(text)
        valor = self._encontra_valor(text).split('(')[0].strip()
        data = self._encontra_data(text)
        
        summary = f"""Contrato entre {partes[0]} e {partes[1]} estabelecido em {data} no valor de {valor[:-2]} com o objetivo de {objeto}""" 
        date = datetime(2022, 11, 21)
        return (summary, date)
        

        return "Resumo Contrato"
    
    
        # encontra partes
    def _encontra_partes(self, total_text):
        padrao = r'(que entre si (celebram|fazem|faz))(.*?) e (.*?)[^,]para'
        correspondencias = re.findall(padrao, total_text, re.IGNORECASE | re.DOTALL)
        if correspondencias:
            p1 = correspondencias[0][2].replace("\n", "")
            p2 = correspondencias[0][3].replace("\n", " ")
            partes = [p1,p2]
            return partes
        else:
            partes = ["||Parte 1 não encontrada||", "||Parte 2 não encontrada||"]
            return partes
    
    #encontra objeto
    def _encontra_objeto(self, total_text):
        #padrao_objeto = r'objeto.*?(contratação.*\n\n)$'
        padrao_objeto = r'objeto.*?(contratação[^.]*.\n)'
        aparicoes = re.findall(padrao_objeto, total_text, re.IGNORECASE | re.DOTALL)
        if aparicoes:
            objeto = aparicoes[0].replace("\n", " ")
            return objeto
        else:
            return "||Objeto não encontrado||"
    
    #econtra valor
    def _encontra_valor(self, total_text):
        padrao_valor = r'((R\$|RS)\s*[\d.,]+\s+\([^)]+\))'
        aparicoes = re.findall(padrao_valor, total_text)
        #verifica se a lista esta vazia
        if not aparicoes:
            valor = "||Valor nao encontrado||"
            return valor
        else:
            valor = aparicoes[0][0]
            valor = valor.replace("\n", " ")
            valor = ' '.join(valor.split())
            return valor
        
    #encontra data
    def _encontra_data(self, total_text):
        padrao_data = r"[A-Z]{2}, (\d{1,2} de [a-zA-ZÀ-ú]+ de \d{4})"
        correspondencias_data = re.findall(padrao_data, total_text, re.IGNORECASE)
        if correspondencias_data:
            data = correspondencias_data[0]
            return data
        else:
            return "||Data não encontrada||"

