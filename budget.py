# -*- coding: utf-8 -*-

import pandas as pd
from benford_law import BenfordLaw
from curva_abc import CurvaABC

class Budget:
  def __init__(self, matrix):
    self.itens_df = pd.DataFrame(matrix)
    #colocando titulo nas colunas.
    self.itens_df.columns = ['Item','Descrição','Und','Quant. Contrato', 'Preço Unitário', 'Preço Total Contrato']
    self.matrix = [l for l in matrix if isinstance(l[2], str)]

    
    
  def compute_metrics(self):
    self.abc = CurvaABC()
    self.abc.fit(self.matrix)
    
    self.benford = BenfordLaw()
    self.benford.fit(self.matrix)
