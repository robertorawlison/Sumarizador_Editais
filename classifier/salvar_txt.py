# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 11:41:37 2024

@author: bruno.bpl
"""

def salvar_em_txt(lista_de_listas, nome_do_arquivo):
    with open(nome_do_arquivo, 'w') as arquivo:
        for lista in lista_de_listas:
            linha = '\t'.join(lista)  # Use '\t' para separar os elementos, mas você pode escolher outro caractere
            arquivo.write(f"{linha}\n")

# Exemplo de uso:
lista_de_listas = [
    ['João', '25', 'Estudante'],
    ['Maria', '30', 'Professora'],
    ['Carlos', '22', 'Programador']
]

nome_do_arquivo = 'dados.txt'
salvar_em_txt(lista_de_listas, nome_do_arquivo)
