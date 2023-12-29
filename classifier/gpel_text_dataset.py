# -*- coding: utf-8 -*-
import spacy, os
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from spellchecker import SpellChecker
from unidecode import unidecode

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
                print(file_path)
                with open(file_path, 'r', encoding="ISO-8859-1", errors="ignore") as file:
                    st = file.read()
                    print(st)
                    self.X.append(st)
                    self.y.append(+1)
        
        # Process files in the non-cover directory
        for filename in os.listdir(non_cover_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(non_cover_dir, filename)
                print(file_path)
                with open(file_path, 'r', encoding="ISO-8859-1", errors="ignore") as file:
                    st = file.read()
                    print(st)
                    self.X.append(st)
                    self.y.append(-1)
    
    
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
    
    
    def _preprocessing(self) -> None:
        '''
        Tratamento de PLN sobre os textos:
            0. Tokenização do texto (separação dos espaços, 
                                     e conversão de maiúsculas em minúsculas); (spacy)
            1. Lematização das plavras; (spacy)
            2. Correção ortográfica; (pyspellchecker)
            3. Remoção dos acentos (minimiza erros do OCR);
            4. Remoção das stop words (lenatizadas e sem acento).
            
        obs: para lidar com dados de teste, é necessário processá-los separadamente dos dados de treino
        usando uma nova chamada do nlp (spacy). Isso garante que o modelo não tenha conhecimento 
        prévio dos dados de teste e ajuda a simular melhor o cenário de aplicação real.
        
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
          
          obs: Ao trabalhar com qualquer técnica de vetorização em aprendizado de máquina, 
          você deve calcular os pesos usando apenas o conjunto de treinamento (TfidfVectorizer.fit(.)) e,
          em seguida, aplicar esses pesos aos dados de teste (TfidfVectorizer.transform(.)). 
          O objeto TfidfVectorizer deve persistir para ser usado na classificação de novos documentos 
          fora do dataset de teste.
          
          Possíveis testes para melhoria da acurácia de classificação:
              Remoção das palavras frequentes no vocabulário. Para a remoção de termos frequentes 
              existem duas possibilidades:
                1. Experiemntal. Determinar qual limiar de frequência mínima
                produz os melhores resultados em instâncias de teste ou validação;
                2. TF-IDF (Term Frequency-Inverse Document Frequency), que 
                levam em conta a importância relativa de uma palavra em 
                relação ao documento e ao corpus.
          

        Returns
        -------
        None.

        '''
        pass
        
    
    
    def posprocessing(self, X : list) -> list:
        '''
        Processa novos dados de documentos fora da base de teste a serem usadas pelo classificador.
        Aplica as técnicas de pré-processamento e vetorização. 
        Na vetorização o objeto que se ajustou ao dados de treinamento deve ser recuperado para manter 
        a base de representação das palavras contidas nos documentos para a hipotese aprendida.
        
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
        list
            Retorna uma matriz de números indicando a importância de cada palavra do vocabulario (coluna)
            no texto de cada documento (linha).
            Ex: X_out = [
                [0.3645444  0.3645444  0.61722732 0.3645444  0. 0. 0.46941728 ]
                [0.41285857 0.41285857 0. 0.41285857 0.69903033 0. 0. ]
                [0.3645444  0.3645444  0. 0.3645444  0. 0.61722732 0.46941728]
                ]
        '''
        pass