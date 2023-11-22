# -*- coding: utf-8 -*-
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import re

from document import Document


class Summarizer:
    def summarize(self, text : str) -> str:
        return ""
    
    @classmethod
    def create_instance(cls, doc : Document):
        if doc.type == Document.DESCONHECIDO :
            return UnknownSummarizer()
        elif doc.type == Document.EDITAL :
            return EditalSummarizer()
        elif doc.type == Document.CONTRATO :
            return ContratoSummarizer()


class UnknownSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        # Crie um analisador de texto
        parser = PlaintextParser.from_string(text, Tokenizer("portuguese"))
    
        # Escolha um método de sumarização (LSA neste exemplo)
        summarizer = LuhnSummarizer()
    
    
        # Obtém um resumo com 1 frase
        return str(summarizer(parser.document, 1)[0])
        

class EditalSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        objetos = self._encontra_objeto(text)
        valor = self._encontra_valor(text).split('(')[0].strip()
        prazo = self._encontra_prazos(text)
        tipo = self._encontrar_tipo(text)

        return f"Edital de licitação na modalidade  {tipo[0]}, cujo objeto trata-se da {objetos[0]}, com valor previsto de {valor} e prazo de execução previsto de {prazo}"


    def _encontra_objeto(self, total_text):
        padrao_objeto = r"contratação[^,]*,"
        objetos = []
        correspondencias = re.findall(padrao_objeto, total_text, re.IGNORECASE)
        if correspondencias: #se a lista nao estiver vazia, correspondencia recebe o primeiro elemento da lista
            correspondencia = correspondencias[0]
            correspondencia_sem_quebras = correspondencia.replace("\n", "").strip()
            posicao_parada = correspondencia_sem_quebras.find(",")
            objeto = correspondencia_sem_quebras[:posicao_parada]
            objetos.append(objeto)
        if objetos:
            return objetos
        else:
            objetos.append("Objeto nao encontrado")
            return objetos
    
    def _encontra_valor(self, total_text):
        padrao_valor = r'((R\$|RS)\s*[\d.,]+\s+\([^)]+\))'
        aparicoes = re.findall(padrao_valor, total_text)
        #verifica se a lista esta vazia
        if not aparicoes:
            valor = "Valor nao encontrado"
            return valor
        else:
            valor = aparicoes[0][0]
            valor = valor.replace("\n", " ")
            valor = ' '.join(valor.split())
            return valor
       
    def _encontra_prazos(self, total_text):
        padrao  = r'prazo.*?execução.*?((\d+)\s*\(([^)]+)\)\s*(dias|meses))'
        correspondencias = re.findall(padrao, total_text, re.IGNORECASE)
    
        if correspondencias:
            prazo = correspondencias[0][0]
        else:
            prazo = "Prazo nao encontrado"
        return prazo
    
    def _encontrar_tipo(self, total_text):
        tipos_possiveis = ["concorrência n", "carta convite n", "tomada de preços n", "pregão eletrônico n", "pregão presencial n", "dispensa de licitação n"]
    
        def encontrar_tipos_de_edital(texto, tipos_possiveis):
            linhas_encontradas = []
            linhas = texto.split("\n")
    
            for idx, linha in enumerate(linhas):
                for tipo in tipos_possiveis:
                    if tipo in linha.lower():
                        linhas_encontradas.append((linha))
                        break
    
            return linhas_encontradas
    
        def encontrar_nome_tipo(texto, tipos_possiveis):
            for tipo in tipos_possiveis:
                if tipo in texto.lower():
                    return tipo
        tipos_encontrados = []
    
        linhas_encontradas = encontrar_tipos_de_edital(total_text, tipos_possiveis)
        tipo = encontrar_nome_tipo(total_text, tipos_possiveis)
        
        tipo_encontrado = False  # Variável para controlar se o tipo foi encontrado
        
        if linhas_encontradas:
            for linha in linhas_encontradas:
                linha_corrigida = " ".join(linha.split())
                if (tipo.strip()) in linha_corrigida.lower() and not tipo_encontrado:
                    a = linha_corrigida.lower().find(tipo)
                    tipo_edital = linha_corrigida[a::]
                    tipos_encontrados.append(tipo_edital)
                    tipo_encontrado = True  # Define como True para evitar mais buscas
        return tipos_encontrados
    
    
    


class ContratoSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        partes = self._encontra_partes(text)
        objeto = self._encontra_objeto(text)
        valor = self._encontra_valor(text).split('(')[0].strip()
        data = self._encontra_data(text)
           
        return f"""Contrato entre {partes[0]} e {partes[1]} estabelecido em {data} no valor de {valor[:-2]} com o objetivo de {objeto}"""
        

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