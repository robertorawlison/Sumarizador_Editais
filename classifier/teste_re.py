# -*- coding: utf-8 -*-

import re

# Exemplo de dados
corpus = ["Isso é uma página 10 de exemplo.",
          "Outra página de exemplo para 1/2039 ilustrar a ideia.",
          "Essa é uma página 1  01/20 diferente."]

for corp in corpus:
    for str in re.findall(r'\bpágina\s\d+\b | \b01/\d+\b | \b1/\d+\b', corp) :
        print(str.replace(" ", ""))
    #print(re.findall(r'\b01/\d+\b|\b1/\d+\b', corp))
    print("\n")

