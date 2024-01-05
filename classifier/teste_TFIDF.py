# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer

# Exemplo de textos tokenizados
textos_tokenizados = [
    ["este", "é", "um", "documento", "de", "exemplo"],
    ["outro", "documento", "de", "exemplo"],
    ["um", "terceiro", "exemplo", "de", "documento"]
]

# Converter listas de tokens de volta para texto
textos_tokenizados_texto = [" ".join(tokens) for tokens in textos_tokenizados]

# Criar objeto TfidfVectorizer e ajustá-lo aos dados tokenizados
vectorizer = TfidfVectorizer()
matriz_tfidf = vectorizer.fit_transform(textos_tokenizados_texto)

# Obter vocabulário e matriz esparsa
vocabulario = vectorizer.get_feature_names_out()
matriz_esparsa = matriz_tfidf.toarray()

# Exibir resultados
print("Vocabulário:", vocabulario)
print("Matriz TF-IDF:")
print(matriz_esparsa)

