# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 12:11:43 2023

@author: bruno.bpl
"""

import os
import spacy
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

class GpelTextDataset:
    '''
    Classe que manipula os dados de texto do datset GPEL
    '''
    def __init__(self, size_test : float = 0.25):
        self.X : list = []
        self.y : list = []
        
        self.X_train : list = None
        self.y_train : list = None
        
        self.X_test : list = None
        self.y_test : list = None
        
        self._load()
        self._split_train_test(size_test)
        self._preprocessing()
        self._vectorization()
        
    
    def _load(self) -> None:
        '''
        Carrega todos os arquivos de texto (.txt) do dataset GPEL
        e adiciona na matriz de textos X associando o mesmo ao rótulo
        y. Se o texto estiver no diretório cover será rotulado com +1,
        se estiver no rótulo non-cover será rotulado com -1
        Returns
        -------
        None.

        '''
        cover_dir = 'dataset/cover'
        non_cover_dir = 'dataset/non-cover'
        
        # Process files in the cover directory
        for filename in os.listdir(cover_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(cover_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    st = file.read()
                    self.X.append(st)
                    self.y.append(+1)
        
        # Process files in the non-cover directory
        for filename in os.listdir(non_cover_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(non_cover_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    st = file.read()
                    self.X.append(st)
                    self.y.append(-1)
                    
    
    