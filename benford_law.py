    # -*- coding: utf-8 -*-
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2

class BenfordLaw: 
    def __init__(self, alpha=0.05):
        self.data = None
        self.alpha = alpha

    def fit(self, matrix):
        self.data = [float(l[5]) for l in matrix]
        self.obs_freq = self.__observed_frequencies()
        self.benfords_freq = self.__benfords_frequencies()
        
        #Teste de hipotese se os dados observados seguem a lei de benford
        # Graus de liberdade (gl)
        #No teste qui-quadrado de ajuste, o grau de liberdade será o número de categorias menos 1,
        #ou seja, 9 - 1 = 8 graus de liberdade. Pois são 9 dígitos com suas frequencias a serem analisadas.
        gl = 8

        # Valor crítico correspondente ao nível de significância (alpha)
        valor_critico = chi2.ppf(1 - self.alpha, gl)
        chi_squared = self.chi_squared_test()
        #Se o valor do teste chi quadrado for maior que o valor crítico então rejeite a hipótese que os dados
        #seguem a Lei de Benford.
        if(valor_critico < chi_squared):
            self.reject_hypothesis = True
        else:
            self.reject_hypothesis = False


    def __observed_frequencies(self):
        #Separa o primeiro dígito de cada observacao
        digits = np.array([int(str(abs(x))[0]) for x in self.data if pd.notnull(x) and x != 0])
        freq = np.zeros(9)
        for digit in digits:
            freq[digit - 1] += 1
        return freq
  
    def __benfords_frequencies(self):
        return [ round(p * len(self.data)) for p in np.log10(1 + 1 / np.arange(1, 10)) ]
  
    def chi_squared_test(self):
        chi_squared = np.sum((self.obs_freq - self.benfords_freq) ** 2 / (self.benfords_freq))
        return chi_squared
  
    def get_figure_plot(self):
        plt.clf()#limpa
        digits = np.arange(1, 10)
  
        n = len(self.data)
        plt.bar(digits, [o/n for o in self.obs_freq], align='center', alpha=0.5, label='Observado')
        plt.plot(digits, [b/n for b in self.benfords_freq], 'r', marker='o', linestyle='-', label='Lei de Benford')
        
        if self.reject_hypothesis == True:
            plt.text(3.2, 0.33, "Anomalia identificada nos dados", color='red')
        else:
            plt.text(2.2, 0.33, "Nenhuma Anomalia identificada nos dados", color='blue')
  
        plt.xlabel('Dígitos principais')
        plt.ylabel('Frequência')
        plt.title('Análise da Lei de Benford')
        plt.legend(loc='center right')
        
        return plt.gcf() 
        
        
    def create_df(self):
        if self.data is None:
            return None
                
        # Create a DataFrame with the values from 1 to 9 in the first column
        #numbers = pd.DataFrame({'Numbers': range(1, 10)})
        
                
        # Calculate the percentage representation of each count
        total_count = len(self.data)
        percentage = [(count / total_count) if total_count > 0 else 0 for count in self.obs_freq]
        theorical_total = sum(self.benfords_freq)
        
        # Calculate the theoretical count and percentage based on Benford's Law
        theoretical_percentage = [(freq / theorical_total) for freq in self.benfords_freq]
        
        # Calculate the absolute difference between occurrences and theoretical count
        absolute_diff = [abs(occ - theo) for occ, theo in zip(self.obs_freq, self.benfords_freq)]
        
        # Calculate the relative difference (percentage) between occurrences and theoretical count
        relative_diff = [(occ - theo) / theo if theo != 0 else 0 for occ, theo in zip(self.obs_freq, self.benfords_freq)]
        
        # Create a new DataFrame with the desired columns
        new_df = pd.DataFrame({
            'Digitos': range(1, 10),
            'Ocorrencias':self.obs_freq,
            'Ocorrencias (%)': percentage,
            'Ocorrencias Lei Benford': self.benfords_freq,
            'Ocorrencias (%) Lei Benford': theoretical_percentage,
            'Diferenca Absoluta': absolute_diff,
            'Diferenca Relativa (%)': relative_diff
        })
        
        # Add total row to the DataFrame
        total_row = pd.DataFrame({
            'Digitos': ['Total'],
            'Ocorrencias': [total_count],
            'Ocorrencias (%)': [sum(percentage)],
            'Ocorrencias Lei Benford': [sum(self.benfords_freq)],
            'Ocorrencias (%) Lei Benford': [sum(theoretical_percentage)],
            'Diferenca Absoluta': [sum(absolute_diff)],
            'Diferenca Relativa (%)': [0]  # No relative difference for the total row
        })
        new_df = pd.concat([new_df, total_row], ignore_index=True)
        
        return new_df
              

