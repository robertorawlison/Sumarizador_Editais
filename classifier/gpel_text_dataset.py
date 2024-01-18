# -*- coding: utf-8 -*-
from typing import Iterable
import os
from sklearn.model_selection import train_test_split

from .gpel_text_preprocessor import GpelTextPreprocessor

class GpelTextDataset:
    '''
    Classe que manipula os dados de texto do datset GPEL
    '''
    def __init__(self):
        self.X : Iterable[str] = []
        self.y : Iterable[str] = []
        
        self.X_train : Iterable[str] = None
        self.y_train : Iterable[str] = None
        
        self.X_test : Iterable[str] = None
        self.y_test : Iterable[str] = None
        
                
    def preprocessing(self) -> None:
        self._load()
        self._preprocessing()
        
    def save_preprocessing(self)  -> None:
        with open("classifier/dataset/data.pre", 'w') as arquivo:
            for lista, label, filename in zip(self.X, self.y, self.file_names):
                linha = filename + '\t' + str(label) + '\t'
                linha += '\t'.join(lista)  # Use '\t' para separar os elementos, mas você pode escolher outro caractere
                arquivo.write(f"{linha}\n")
        
    
    def load_preprocessing(self, size_test : float = 0.25) -> None:
        with open("classifier/dataset/data.pre", 'r', encoding="ISO-8859-1", errors="ignore") as arquivo:
            for linha in arquivo:
                elementos = linha.strip().split('\t')
                self.y.append(int(elementos[1])) #Ignora o nome do arquivo original que está na primeira posição
                self.X.append(' '.join(elementos[2:]))
        
        self._split_train_test(size_test)
        
        
        
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
        cover_dir = 'classifier/dataset/cover'
        non_cover_dir = 'classifier/dataset/non-cover'
        
        self.file_names = [] #Nome do arquivo de cada instância do dataset
        # Process files in the cover directory
        for filename in os.listdir(cover_dir):
            if filename.endswith('.txt'):
                self.file_names.append(filename)
                file_path = os.path.join(cover_dir, filename)
                #print(file_path)
                with open(file_path, 'r', encoding="ISO-8859-1", errors="ignore") as file:
                    st = file.read()
                    #print(st)
                    self.X.append(st)
                    self.y.append(+1)
        
        #Process files in the non-cover directory
        for filename in os.listdir(non_cover_dir):
            if filename.endswith('.txt'):
                self.file_names.append(filename)
                file_path = os.path.join(non_cover_dir, filename)
                #print(file_path)
                with open(file_path, 'r', encoding="ISO-8859-1", errors="ignore") as file:
                    st = file.read()
                    #print(st)
                    self.X.append(st)
                    self.y.append(-1)
         
            
    
    def _split_train_test(self, test_size: float):
        '''
        Quebra a instância X em X_train, usado na fase de aprendizado do dados, e em X_test
        a ser usada na computação das métricas de classificação e comparação com outros modelos.

        Parameters
        ----------
        test_size : float
            Indica a proporção de dados da matriz X que irá compor a matriz X_test, 
            sendo o resto colocado na matriz X_train.

        Returns
        -------
        None.

        '''
        # Usar train_test_split para dividir os dados em treino e teste
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, 
                                                                                self.y, 
                                                                                test_size=test_size, 
                                                                                random_state=42)

        print(f"Tamanho de X_train: {len(self.X_train)}")
        print(f"Tamanho de X_test: {len(self.X_test)}")
        print(f"Tamanho de y_train: {len(self.y_train)}")
        print(f"Tamanho de y_test: {len(self.y_test)}")
    
    
    def _preprocessing(self) -> None:
        '''
        Tratamento de PLN sobre os textos com auxílio do objeto GpelTextPreprocessor
        Returns
        -------
        None.

        '''
        preprocessor = GpelTextPreprocessor()
        #self.X = preprocessor.transform(self.X)

        for text, label, filename in zip(self.X, self.y, self.file_names):
            lista = preprocessor.process_text(text)
            with open("classifier/dataset/data.pre", 'a') as arquivo:
                linha = filename + '\t' + str(label) + '\t'
                linha += '\t'.join(lista)  # Use '\t' para separar os elementos, mas você pode escolher outro caractere
                arquivo.write(f"{linha}\n")