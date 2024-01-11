# -*- coding: utf-8 -*-
from typing import Iterable
import spacy
from spellchecker import SpellChecker

class GpelTextPreprocessor:
    '''
    Classe que pré processa os textos dos documentos do dataset GPEL
    '''
    def __init__(self):
        self.count = 0
        self.nlp : spacy.lang.pt = None
        self.spell : SpellChecker = None
        self._init_portuguese_model()
      
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
        
    
    def transform(self, X : Iterable[str]) -> Iterable[Iterable[str]]:
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
        
        

        Returns
        -------
        Iterable[Iterable[str]]
            A matriz X resultante é uma lista de textos tratados, onde cada 
            texto é uma lista de strings
                X=[['três', 'dois', 'apoio', 'sobre', 'algo'],
                   ['querer', 'tende', 'dezanove', 'eles']
                   ]

        '''
        
        # Aplicar o processamento em cada documento de X
        return [self.process_text(doc) for doc in X]


    def process_text(self, text : str) -> Iterable[str]:
        print("Processando página " + str(self.count))
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