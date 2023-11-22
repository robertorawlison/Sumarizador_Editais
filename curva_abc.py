# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Calcule a derivada segunda usando diferença central
def central_difference(x, y):
    n = len(x)
    dx = x[1] - x[0]
    d2y = [(y[i-1] - 2*y[i] + y[i+1]) / (dx**2) for i in range(1, n-1)]
    return d2y


def get_inflection_point(x, y):
    # Aplica a função para calcular a derivada segunda
    d2y = central_difference(x, y)

    # Encontre os índices onde a derivada segunda se aproxima de zero
    zero_indices = np.where(np.isclose(d2y, 0.0))
    
    # Primeiro ponto onde a derrivada segunda é proxima de zero
    i = zero_indices[0][0]
    zero_point = (x[i+1], y[i+1]) # Índice + 1 para compensar a diferença central
    print(f"x = {zero_point[0]}")
    print(f"y = {zero_point[1]}")

    return zero_point



class CurvaABC:
    def __init__(self):
        self.data = None


    def fit(self, matrix):
        self.data = matrix.copy()
    
        # Sort the data frame based on the last column (ignoring the first row)
        self.data = sorted(self.data, key=lambda linha: linha[5], reverse=True)

        #Converte a string dos preços em vetor de floats
        precos = [float(l[5]) for l in self.data]
    
        #Adicionando metricas acumulativas na tabela ABC
        self.p_individual = [0] * len(precos) #Porcentagem individual de cada preço
        self.p_acumulada = [0] * len(precos)
        self.preco_acumulado = [0] * len(precos)
    
        soma_preco = sum(precos)
    
        variacao_minima = 1 / len(precos)
        
        for i, preco in enumerate(precos):
            self.p_individual[i] = preco / soma_preco
            if (i == 0):
                self.p_acumulada[i] = self.p_individual[i]
                self.preco_acumulado[i] = preco
            else:
                self.p_acumulada[i] = self.p_acumulada[i-1] + self.p_individual[i]
                self.preco_acumulado[i] = self.preco_acumulado[i-1] + preco
        
        #Região Variação Mínima
        self.ponto_vm = get_inflection_point([i+1 for i in range(len(precos))], self.p_acumulada)
# =============================================================================
#         for i, p in enumerate(self.p_individual):
#             if p < variacao_minima:
#                 self.ponto_vm = (i+1, self.p_acumulada[i])
#                 break
# =============================================================================
               
            
        #Encontrando as regiões AB
        #Região A
        item = 1
        v = 0
        while(item <= len(self.p_acumulada)):
            v = self.p_acumulada[item-1]
            if v >= 0.8:
                self.ponto_a = (item, v)
                break
            item += 1
        #Regiao B
        while(item <= len(self.p_acumulada)):
            v = self.p_acumulada[item-1]
            if v >= 0.9:
                self.ponto_b = (item,v)
                break
            item += 1
    
        
    def create_df(self):    
        #Fazendo a transposta da matriz com os dados
        data = list(zip(*self.data))
        # Create a new DataFrame with the desired columns
        abc_df = pd.DataFrame({
            'Itens': data[0],
            'Descrição': data[1],
            'Und': data[2],
            'Quant. Contrato': data[3],
            'Preço Unitário': data[4],
            'Preço Total Contrato': data[5],
            'Percentual unitário': self.p_individual,
            'Valores acumulados': self.preco_acumulado,
            'Percentual acumulado': self.p_acumulada
        })
        return abc_df
    
    def get_figure_plot(self):
        plt.clf()#limpa
        plt.ylim(bottom=0)
        # Criar o gráfico de linha
        x = [0] + [i+1 for i in range(len(self.p_acumulada))]
        y = [0] + self.p_acumulada
        plt.plot(x, y)
        
        #Região Variação Mínima
        plt.plot([self.ponto_vm[0],self.ponto_vm[0]],[0, self.ponto_vm[1]], color='red')
        text_vm = str("{:.1%}".format(self.ponto_vm[1]))
        plt.text(self.ponto_vm[0], 0.9, text_vm, color='red')
        
        #Região A
        plt.plot([self.ponto_a[0],self.ponto_a[0]],[0, self.ponto_a[1]], color='black')
        text_a = str("{:.1%}".format(self.ponto_a[0] / len(self.p_acumulada)))
        plt.text(self.ponto_a[0]/5, self.ponto_a[1]/4, text_a)
        
        #Regiao B
        plt.plot([self.ponto_b[0],self.ponto_b[0]],[0, self.ponto_b[1]], color='black')
        text_b = str("{:.1%}".format((self.ponto_b[0] - self.ponto_a[0]) / len(self.p_acumulada)))
        plt.text(self.ponto_b[0]*2/3, self.ponto_b[1]/3, text_b)
               
        #Regiao C
        x_c = self.ponto_b[0] + (len(self.p_acumulada) - self.ponto_b[0]) // 2
        text_c = str("{:.1%}".format(1 - (self.ponto_b[0] / len(self.p_acumulada))))
        plt.text(x_c, self.ponto_b[1]/2, text_c)
        
        # Adicionar rótulos aos eixos x e y
        plt.xlabel('Número de itens')
        plt.ylabel('Percentual Acumulada')
        
        # Adicionar título ao gráfico
        plt.title('Curva ABC')
        #plt.show()
        
        return plt.gcf() 

