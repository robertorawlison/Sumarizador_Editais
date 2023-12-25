# -*- coding: utf-8 -*-
import spacy

# Carregar o modelo para o português
nlp = spacy.load("pt_core_news_sm")


stopwords_portuguese = nlp.Defaults.stop_words #stop words
text = " ".join(stopwords_portuguese) #junta palavras em uma única string
doc = nlp(text) #Lematiza as palavras

# Lematiza as stop words e remove as repetições
stopwords_portuguese_set = set()
for token in doc:
    stopwords_portuguese_set.add(token.lemma_)

print(len(stopwords_portuguese), len(stopwords_portuguese_set))
print(stopwords_portuguese_set)

