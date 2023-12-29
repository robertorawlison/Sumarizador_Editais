# -*- coding: utf-8 -*-
import spacy
from unidecode import unidecode

# Carregar o modelo para o português
nlp = spacy.load("pt_core_news_sm")

text = "Onde houver ódio que eu leve o amor. João, cadê você?"

# Exemplo de uso
texto_sem_acentos = unidecode(text)

print(f"Original: {text}")
print(f"Sem acentuação: {texto_sem_acentos}")


doc = nlp(text) #Lematiza as palavras
for token in doc:
    if not token.is_punct: #Testa se token não é uma pontuação 
        print(token.lemma_)


#Teste com stopwords
stopwords_portuguese = nlp.Defaults.stop_words #stop words
text = " ".join(stopwords_portuguese) #junta palavras em uma única string
doc = nlp(text) #Lematiza as palavras

# Lematiza as stop words e remove as repetições
stopwords_portuguese_set = set()
for token in doc:
    stopwords_portuguese_set.add(token.lemma_)

print(len(stopwords_portuguese), len(stopwords_portuguese_set))
print(stopwords_portuguese_set)

