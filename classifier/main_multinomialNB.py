# -*- coding: utf-8 -*-
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

from gpel_text_dataset import GpelTextDataset


def vectorization(dataset : GpelTextDataset):
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
            1. Experimental. Determinar qual limiar de frequência mínima
            produz os melhores resultados em instâncias de teste ou validação;
            2. TF-IDF (Term Frequency-Inverse Document Frequency), que 
            levam em conta a importância relativa de uma palavra em 
            relação ao documento e ao corpus.
      

    Returns
    -------
    X_train, y_train, X_test, y_test.

    '''
    pass



if __name__ == "__main__":
    dataset = GpelTextDataset()
    dataset.load_train_test()
   
    X_train, y_train, X_test, y_test = vectorization(dataset) 
   
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    
    y_prob = mnb.predict_proba(X_test)
    #print(y_prob)
    y_pred = mnb.predict(X_test)
    #print(y_pred)
    
    print(classification_report(y_test, y_pred))

