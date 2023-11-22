# -*- coding: utf-8 -*-

import tabula
import numpy as np
from budget import Budget

class BudgetPDFReader:
    def __init__(self, file_name):
        self.file_name = file_name
        
    def read(self):
        tabula_tables = tabula.read_pdf(self.file_name, pages="all")
    
        M_filtrado = []
        first_table = True
        
        for table in tabula_tables:
            M = table.values
        
            # para que nao repita o cabecalho 
            if first_table:
                start_row = 1
                first_table = False
            else:
                start_row = 2  
        
            #Filtrando as linhas cujo valor inicial não é uma string
            atividade = None
            for i in range(start_row, len(M)):
                #Trata números da terceira coluna que estão vindo
                #colocados com os valores da quarta coluna
                if isinstance( M[i][3], str) and ' ' in M[i][3]:
                    split_string = M[i][3].split(' ')
                    M[i][3] = split_string[0]
                    M[i][4] = split_string[-1]
                
                valorInicial = M[i][0]
        
                if isinstance(valorInicial, str) == False:
                  if isinstance(M[i][1], str):
                      descricao = str(M[i][1])
                      if atividade != None:
                        atividade += "\n" + descricao
                      else:
                        atividade = descricao
                else:
                    if atividade == None:
                      M[i][1] = str(M[i][1])
                    else:
                        M[i][1] = atividade + "\n" + str(M[i][1])
                    for col in [3,4,5]:
                        if isinstance( M[i][col], str):
                            valor = M[i][col].replace(".", "").replace(",", ".")
                            M[i][col] = float(valor)
        
                    M_filtrado.append(M[i])
                    atividade = None

        budget = Budget(M_filtrado)
        return budget