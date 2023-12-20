# -*- coding: utf-8 -*-
import re
from datetime import datetime
from .summarizer import Summarizer

class EditalSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        objetos = self._encontra_objeto(text)
        valor = self._encontra_valor(text).split('(')[0].strip()
        prazo = self._encontra_prazos(text)
        tipo = self._encontrar_tipo(text)

        date = Summarizer._encontra_data(self, text)

        if date == datetime.max:
            data = "||Desconhecido||"
        else:
            data = date.strftime("%d/%m/%Y")

        summary = f"Edital de licitação na modalidade  {tipo[0]}, cujo objeto trata-se da {objetos[0]}, com valor previsto de {valor} e prazo de execução previsto de {prazo}"
        return (summary, date) 


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