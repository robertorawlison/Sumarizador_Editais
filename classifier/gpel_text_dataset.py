# -*- coding: utf-8 -*-

import spacy
from sklearn.feature_extraction import DictVectorizer
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
        self._preprocessing()
        self._vectorization()
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
        pass
    
    
        '''
            Para cada arquivo .txt dos diretórios dataset/cover e dataset/non-cover
                st = todo o conteúdo de arquivo
                self.X.append(st)
                if arquivo estiver em cover
                    self.y.append(+1)
                else
                    self.y.append(-1)
            
        '''
    
    
    
    def _preprocessing(self) -> None:
        '''
        Tratamento de PLN sobre os textos:
            1. Lematização das plavras; (spacy)
            2. Remoção dos acentos (minimiza erros do OCR);
            3. Remoção das stop words (lenatizadas e sem acento);
            4. Remoção das palavras frequentes no vocabulário. Para a remoção
            de termos frequentes existem duas possibilidades:
                4.1 Experiemntal. Determinar qual limiar de frequência mínima
                produz os melhores resultados em instâncias de teste ou validação;
                4.2 TF-IDF (Term Frequency-Inverse Document Frequency), que 
                levam em conta a importância relativa de uma palavra em 
                relação ao documento e ao corpus.
        
        A matriz X resultante é uma lista de textos tratados, onde cada 
        texto é uma lista de strings
        X=[['três', 'dois', 'apoio', 'sobre', 'algo'],
           ['querer', 'tende', 'dezanove', 'eles']
            ]

        Returns
        -------
        None.

        '''
        pass


        
    def _vectorization(self):
        '''
          Converte o texto em uma representação numérica que os algoritmos de 
          aprendizado de máquina possam entender.
          
          Cada texto é representado por um vetor no qual cada componente 
          corresponde à frequência de uma palavra específica no vocabulário.
          Esse método é conhecido como Bag of Words. E pode ser implementado 
          com a classe DictVectorizer do pacote sklearn.feature_extraction.
          
          Outras técnicas de vetorização incluem o uso de esquemas mais avançados, 
          como o TF-IDF (Term Frequency-Inverse Document Frequency) ou a representação 
          de palavras usando embeddings, como Word2Vec ou GloVe.
          

        Returns
        -------
        None.

        '''
        pass
        
    def _split_train_test(self, test_size : float):
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
        pass
        
