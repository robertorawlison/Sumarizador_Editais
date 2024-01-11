# -*- coding: utf-8 -*-
from typing import Iterable
from sklearn.pipeline import Pipeline
import pickle

from gpel_text_preprocessor import GpelTextPreprocessor

class GpelTexClassifier:
    '''
    Classe que manipula os dados de texto do datset GPEL
    '''
    def __init__(self):
       self.classifier : Pipeline = None 
                
       
    def save(self) -> None:
        '''
          Persiste em arquivo o objeto de vetorização e o classificador melhor ajustados ao dataset
          durante a fase de trenamento. Estes objetos devem ser utilizados em novas instâncias fora do 
          dataset de treino e teste.

        Returns
        -------
        None.

        '''
        with open('model/model.pkl', 'wb') as file:
            pickle.dump(self.classifier, file)
        
        
    def load(self)  -> None:
        '''
          Carrega de arquivo o objeto de vetorização e o classificador melhor ajustados ao dataset 
          durante a fase de trenamento. Estes objetos devem ser utilizados em novas instâncias fora 
          do dataset de treino e teste.

        Returns
        -------
        None.

        '''
        with open('model/model.pkl', 'rb') as file:
            self.classifier = pickle.load(file)
        
        
    
    def predict(self, X : Iterable[str]) -> Iterable[int]:
        '''
        Processa novos textos de documentos (fora da base de treino/teste), vectorizando e classificando
        em CAPA e NÃO-CAPA.
        
        Aplica as técnicas de pré-processamento, vetorização e classificação. 
        Na vetorização e na classificação os objetos que se ajustaram melhor aos dados de treinamento 
        são recuperado para manter a base de representação das palavras contidas nos documentos para a 
        hipotese aprendida.
        
        Parameters
        ----------
        X : list
            Lista de textos de documentos a serem classificados.
            Ex: X = [
                "Este é um texto de teste",
                "Outro texto de teste"
                ].

        Returns
        -------
        Iterable[int]
            Retorna um vetor de classificação dos textos fornecidos como entrada. 
            Retorna valor +1 para classificar o texto como uma capa e -1 como não-capa.
        '''
        
        processor = GpelTextPreprocessor()
        X_words = processor.transform(X)
        return self.classifier.predict(X_words)
       
    

