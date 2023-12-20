# -*- coding: utf-8 -*-
import re
from datetime import datetime
from .summarizer import Summarizer
from collections import Counter

class AditivoSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        contrato = self._encontra_n_contrato(text)
        tipo = self._encontra_tipo(text)
        
        date = Summarizer._encontra_data(self, text)

        if date == datetime.max:
            data = "||Desconhecido||"
        else:
            data = date.strftime("%d/%m/%Y")

        if tipo == "prazo e valor":
            prazo = self._encontra_prazo(text)
            valor = self._encontra_valor(text)
            summary = f'Termo aditivo de {tipo} do contrato Nº {contrato} estabelecido em {data} com adição do prazo de {prazo} e com modificação do valor para {valor}'
        elif tipo == "prazo":
            prazo = self._encontra_prazo(text)
            summary = f'Termo aditivo de {tipo} do contrato Nº {contrato} estabelecido em {data} com adição do prazo de {prazo}'
        elif tipo == "valor":
            valor = self._encontra_valor(text)
            summary = f'Termo aditivo de {tipo} do contrato Nº {contrato} estabelecido em {data} com modificação do valor para {valor}'

        
        return (summary, date) 
    
    def encontrar_valor_mais_frequente(self, lista):
        contagem = Counter(lista)
        valor_mais_frequente = contagem.most_common(1)[0][0] # Pega o primeiro elemento da lista de tuplas em caso de empate
        return valor_mais_frequente

    def _encontra_n_contrato(self, total_text):
    
        padrao1 = r'CONTRATO\s*(\d+(?:[.,\s]*\d+)?/\d{4})'
        padrao2 = r'CONTRATO\s*PJ\s*-\s*(\d+(?:[.,\s]*\d+)?/\d{4})'
        padrao3 = r'(?:CONTRATO|CT).{0,25} N[º°*,\.]+.*?[^0-9]*(\d+(?:[.,\s]*\d+)?/\d{4})'

        aparicoes_padrao1 = re.findall(padrao1, total_text, re.IGNORECASE|re.DOTALL)
        if aparicoes_padrao1:
            return self.encontrar_valor_mais_frequente(aparicoes_padrao1)

        aparicoes_padrao2 = re.findall(padrao2, total_text, re.IGNORECASE|re.DOTALL)
        if aparicoes_padrao2:
            return self.encontrar_valor_mais_frequente(aparicoes_padrao2)
        
        aparicoes_padrao3 = re.findall(padrao3, total_text, re.IGNORECASE | re.DOTALL)
        if aparicoes_padrao3:
            return self.encontrar_valor_mais_frequente(aparicoes_padrao3)


        return "||contrato não encontrado||"    
    
    
    
    def _encontra_tipo(self, total_text):
        padrao_prazo_1 = r'(?:(?:prorrogação+\sde+\sprazo|aditivo+\sde+\sprazo|prorrogação+\sda+\svigência|prorrogar+\sa+\svigência|prorrogando+\ssua+\svigência|prorrogação+\sdos+\sprazos|prorrogação+\spelo+\sprazo+\sde+\svigência))'
        padrao_prazo_2 = r'os\s+prazos\s+previstos.*ficam\s+prorrogados'
        padrao_valor_1 = r'(?:(?:correção+\sda+\splanilha+\sorçamentaria|alterado+\so+\svalor|acréscimo+\sde+\sserviço|alterar+\so+\svalor|termo+\saditivo+\sprazo-+\sde+\svalor|passando\s+o\s+valor))'
        padrao_valor_2 = r'o\s+valor\s+previsto.*sofrerá'

        aparicoes_prazo_1 = re.search(padrao_prazo_1, total_text, re.IGNORECASE)
        aparicoes_prazo_2 = re.search(padrao_prazo_2, total_text, re.IGNORECASE|re.DOTALL)
        aparicoes_valor_1 = re.search(padrao_valor_1, total_text, re.IGNORECASE)
        aparocoes_valor_2 = re.search(padrao_valor_2, total_text, re.IGNORECASE|re.DOTALL)

        if (aparicoes_prazo_1 or aparicoes_prazo_2) and (aparicoes_valor_1 or aparocoes_valor_2):
            return 'prazo e valor'

        elif aparicoes_prazo_1 or aparicoes_prazo_2:
            return 'prazo'
        elif aparicoes_valor_1 or aparocoes_valor_2:
            return 'valor'
        else:
            return '||Tipo não encontrado||'
        

    def _encontra_valor(self, total_text):
        padrao1 = r'passando\s+o\s+valor.*para\s*((?:R\$|RS)+\s*[\d.,]+)\s*(?:\()'
        padrao2 = r'(?:passará|passa)+\s+de+\s*(?:(?:R\$|RS)+\s*[\d.,]+\s*\([^)]+\))+\s+para.*((?:R\$|RS)+\s*[\d.,]+)\s*(?:\()'
        padrao3 = r'perfazendo\s+um\s+total.*de+\s((?:R\$|RS)+\s*[\d.,]+)\s*(?:\()'
        aparicoes1 = re.findall(padrao1, total_text, re.IGNORECASE|re.DOTALL)
        aparicoes2 = re.findall(padrao2, total_text, re.IGNORECASE|re.DOTALL)
        aparicoes3 = re.findall(padrao3, total_text, re.IGNORECASE|re.DOTALL)
        if aparicoes1:
            valor = aparicoes1[0].replace("\n"," ")
            return valor
        elif aparicoes2:
            valor = aparicoes2[0].replace("\n"," ")
            return valor
        elif aparicoes3:
            valor = aparicoes3[0].replace("\n"," ")
            return valor
        else:
            return '||Valor não encontrado||'
        
    def _encontra_prazo(self, total_text):
        padrao = r'(?:prorrogado|prorrogados|prorrogada|acrescido|prorrogando|prorroga-se|protrogado|aditado|promogada|promrogado|prorogado|prorrogação|promrogação?)\D*([^\d]*(\d+.*?(?:dias|meses|mecses|mesos)))'
        aparicoes = re.findall(padrao, total_text, re.IGNORECASE)
        
        prazo_filtrado = []
        for item in aparicoes: 
            if len(item[1]) < 45:
                prazo_filtrado.append(item[1].strip())  # Filtra as aparições com menos de 45 caracteres e remove espaços extras
        
        if prazo_filtrado:
            return prazo_filtrado[0]
        else:
            return "||Prazo não encontrado||"