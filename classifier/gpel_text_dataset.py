# -*- coding: utf-8 -*-
from typing import Iterable
import spacy, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from spellchecker import SpellChecker

class GpelTextDataset:
    '''
    Classe que manipula os dados de texto do datset GPEL
    '''
    def __init__(self, ):
        self.count = 0
        self.X : list = []
        self.y : list = []
        
        self.X_train : list = None
        self.y_train : list = None
        
        self.X_test : list = None
        self.y_test : list = None
        
                
    def preprocessing(self, size_test : float = 0.25):
        self._load()
        self._preprocessing()
        self._split_train_test(size_test)
        
    def save_preprocessing(self):
        with open("dataset/data.pre", 'w') as arquivo:
            for lista, label, filename in zip(self.X, self.y, self.file_names):
                linha = filename + '\t' + str(label) + '\t'
                linha += '\t'.join(lista)  # Use '\t' para separar os elementos, mas você pode escolher outro caractere
                arquivo.write(f"{linha}\n")
        
    
    def load_preprocessing(self, size_test : float = 0.25) -> None:
        with open("dataset/data.pre", 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                elementos = linha.strip().split('\t')
                self.y.append(int(elementos[1])) #Ignora o nome do arquivo original que está na primeira posição
                self.X.append(elementos[2:])
        
        self._split_train_test(size_test)
        
      
    def _init_portuguese_model(self) -> None:
        # Inicializar o modelo Spacy para o idioma Português
        self.nlp = spacy.load('pt_core_news_sm')
        self.spell = SpellChecker(language='pt')
        
        #Lemmatizando as stop-words
        stopwords_portuguese = self.nlp.Defaults.stop_words #stop words
        doc = self.nlp(" ".join(stopwords_portuguese)) #Lematiza as palavras

        # Lematiza as stop words e remove as repetições
        self.stopwords_portuguese_set = set()
        for token in doc:
            self.stopwords_portuguese_set.add(token.lemma_)
        
        #Adição de stopwords locais
        self.stopwords_portuguese_set.add("paraíba")
        self.stopwords_portuguese_set.add("pb")
        
        
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
        Tratamento de PLN sobre os textos:
            1. Remoção da acentuação (minimiza erros do OCR) (unicode)
            2. Tokenização do texto (separação dos espaços, 
                                     e conversão de maiúsculas em minúsculas); (spacy)
            3. Lematização das palavras; (spacy)
            4. Correção ortográfica; (pyspellchecker);
            5. Remoção das stop words (lematizadas e sem acento).
            
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
        self._init_portuguese_model()
        
        # Aplicar o processamento em cada documento de X
        self.X = [self.process_text(doc) for doc in self.X]


    def process_text(self, text : str) -> Iterable[str]:
        print("Processando documento " + str(self.count))
        self.count += 1
        
        # 0. Colocar todos os caracteres para minúsculo
        text_lower = text.lower()
        #print(text_lower)
        
        # 1. Tokenização do texto
        doc = self.nlp(text_lower)
        #print(len(doc))
        #print("Tokenização")
        #for token in doc:
        #    print(f"{token.text}: {token.lemma_} : {token.pos_}")
        #print("\n\n")
        
        # 2. Lematização das palavras, removendo pontuações.
        lemmatized_words = [token.lemma_ for token in doc if token.pos_ == 'ADJ' #Adjetivo
                                                            or token.pos_ == 'ADV' #Advérbio
                                                            or token.pos_ == 'AUX' #Verbo auxiliar
                                                            or token.pos_ == 'NOUN' #Substantivo
                                                            or token.pos_ == 'PRON' #Pronome
                                                            or token.pos_ == 'VERB'] #Verbo
        #print(lemmatized_words)
        
        if len(lemmatized_words) == 0 :
            return []
        #print(lemmatized_words)
        #print("\n\n\n")
        
        # 3. Correção ortográfica e remoção da acentuação
        unknown_words = self.spell.unknown(lemmatized_words)
        corrected_words = []
        for word in lemmatized_words:
            if word in unknown_words: #unknown_words é um set. pesquisa eficiente
                correc = self.spell.correction(word)
                if(correc != None):
                    doc = self.nlp(correc) # Obter o lemma da palavra corrigida
                    corrected_words.append(doc[0].lemma_)
            else:
                corrected_words.append(word)
        
        #Remove palavras que não contenham dígitos e com apenas uma letra
        corrected_words = [word for word in corrected_words if word.isalpha() and len(word) > 1]
        
        

        # 4. Remoção das stop words lematizadas
        final_result = [word for word in corrected_words if word not in self.stopwords_portuguese_set]
        
        #print("Resultado final sem números")
        print(final_result)
        #print(len(final_result))

        return final_result

        
    def save_vectorization(self, vect : TfidfVectorizer):
        '''
          Persiste em arquivo o objeto de vetorização utilizado durante a fase de trenamento.
          Este objeto deve ser utilizado em novas instâncias fora do dataset de treino e teste.

        Returns
        -------
        None.

        '''
        pass
        
    def _load_vectorization(self):
        '''
          Carrega de arquivo o objeto de vetorização utilizado durante a fase de trenamento.
          Este objeto deve ser utilizado em novas instâncias fora do dataset de treino e teste.

        Returns
        -------
        None.

        '''
        self.vect = None
    
    
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
        self._init_portuguese_model()
        self._load_vectorization()