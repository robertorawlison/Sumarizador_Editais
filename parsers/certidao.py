import re
from datetime import datetime
from .summarizer import Summarizer

class CertidaoSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        tipo = self._encontra_tipo_cetidao(text)
        empresa = self._encontra_empresa(text)
        validade = self._encontra_validade(text)

        date = Summarizer._encontra_data(self, text)

        if date == datetime.max:
            data = "||Desconhecido||"
        else:
            data = date.strftime("%d/%m/%Y")

        summary = f"""Certidão {tipo}, com data de validade de/até {validade}, em nome da empresa {empresa}.""" 
        return (summary, date)

    def _encontra_tipo_cetidao(self, total_text):
        padrao_certidao = r'(?i)CERTIDÃO POSITIVA'
        padrao_efetiva_negativa = r'(?i)COM EFEITO DE NEGATIVA|COM EFEITOS DE MEGATIVA|EFEITOS DE NEGATIVA'
        padrao_certidao_negativa = r'(?i)CERTIDÃO NEGATIÍIVA|CERTIDÃO NEGATIVA'
        padrao_certidao_regular = r'(?i)REGULAR|REGULARIDADE'


        correspondencia_certidao_positiva = re.search(padrao_certidao, total_text, re.IGNORECASE)
        correspondencia_efetiva_negativa = re.search(padrao_efetiva_negativa, total_text, re.IGNORECASE)
        correspondencia_certidao_negativa = re.search(padrao_certidao_negativa, total_text, re.IGNORECASE)
        correspondencia_certidao_regular = re.search(padrao_certidao_regular, total_text, re.IGNORECASE)

        if correspondencia_certidao_positiva and correspondencia_efetiva_negativa:  
            return "positiva com efeito de negativa"

        elif correspondencia_certidao_negativa:
            return "negativa"
        
        elif correspondencia_certidao_regular:
            return "regularidade"
        
        else:
            return "||Tipo não encontrado||"
        
    def _encontra_empresa(self, total_text):
        padrao1 = r'nome: (.*?)(?:CNPJ|CNDI|C.N.P.J|CPF)'
        aparicoes1 = re.findall(padrao1, total_text, re.IGNORECASE|re.DOTALL)
        padrao2 = r'(?:razão social:|razão.*al)(.*?)$'
        aparicoes2 = re.findall(padrao2, total_text, re.IGNORECASE|re.MULTILINE)
        padrao3 = r'(?:nome empresarial|nome.*ial)(.*?)(?:endereço|capital social|protocolo|título)'
        aparicoes3 = re.findall(padrao3, total_text, re.IGNORECASE|re.DOTALL)
        padrao4 = r'Nome do Contribuinte\n\d+\s(.*?)Endereço'
        aparicoes4 = re.search(padrao4, total_text, re.IGNORECASE|re.DOTALL)


        if aparicoes1:
            aparicoes1 = aparicoes1[0].replace("\n", "").strip()
            return aparicoes1
        elif aparicoes2:
            aparicoes2 = aparicoes2[0].replace("\n", "").strip()
            return aparicoes2
        elif aparicoes3:
            aparicoes3 = aparicoes3[0].replace("\n", "").strip()
            return aparicoes3
        elif aparicoes4:
            return aparicoes4.group(1)
        else:
            return "||Empresa não encontrada"
        
    def _encontra_validade(self, total_text):
        padrao_1 = r'(?:(?:vá|va)lida até|validade: ).*?(\d{2}/\d{2}/\d{4}).*$'
        aparicoes1 = re.findall(padrao_1, total_text, re.IGNORECASE|re.DOTALL|re.MULTILINE)
        padrao_2 = r'(?:(?:vá|va)lida por|prazo de)\s+(\d+)(?:.*?dias)'
        aparicoes2 = re.findall(padrao_2, total_text, re.IGNORECASE|re.DOTALL|re.MULTILINE)
        padrao_3 = r'(?:validade:\d{2}/\d{2}/\d{4}).*(?:a|à) (\d{2}/\d{2}/\d{4})'
        aparicoes3 = re.findall(padrao_3, total_text, re.IGNORECASE|re.DOTALL|re.MULTILINE)
        padrao_4 = r'(?:ida até )(\d{2}/\d{2}/\d{4}).*$'
        aparicoes4 = re.findall(padrao_4, total_text, re.IGNORECASE|re.DOTALL|re.MULTILINE)

        if aparicoes1:
            #print("tipo 1")
            return aparicoes1[0]
        elif aparicoes2:
            #print("tipo 2")
            aparicoes2[0] += "dias"
            return aparicoes2[0]
        elif aparicoes3:
           #print("tipo 3")
            return aparicoes3[0]
        elif aparicoes4:
            #print("tipo 4")
            return aparicoes4[0]
        else:
            return "||Validade não encontrada||"
        
