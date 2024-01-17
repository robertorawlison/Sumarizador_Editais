# -*- coding: utf-8 -*-

from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.metrics import classification_report

from gpel_text_dataset import GpelTextDataset
from gpel_text_classifier import GpelTexClassifier


if __name__ == "__main__":

    dataset = GpelTextDataset()
    dataset.load_preprocessing()
    
    # Criar um pipeline com TfidfVectorizer e MultinomialNB
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    
    # Definir a grade de hiperparâmetros a serem testados
    parametros_grid = {
        'tfidf__max_features': [100, 150, 250, 350, None],
        'clf__alpha': [0.1, 0.5, 1.0]
    }
    
    # Inicializar a busca em grade com validação cruzada
    grid_search = GridSearchCV(pipeline, parametros_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=2)
    
    # Executar a busca em grade no conjunto de treinamento
    print(dataset.X_train[0])
    grid_search.fit(dataset.X_train, dataset.y_train)
    
    # Exibir os melhores hiperparâmetros encontrados
    print("Melhores Hiperparâmetros:")
    print(grid_search.best_params_)
    
    # Exibir a melhor pontuação de validação cruzada
    print(f'Melhor Pontuação de Acurácia: {grid_search.best_score_:.4f}')
    
    # Persistindo o classificador que melhor se ajustou aos dados
    gtc = GpelTexClassifier()
    gtc.classifier = grid_search.best_estimator_
    gtc.save()
    
    # Fazer previsões no conjunto de teste
    y_pred_test = gtc.classifier.predict(dataset.X_test)

    # Avaliar o desempenho no conjunto de teste
    acuracy_test = metrics.accuracy_score(dataset.y_test, y_pred_test)
    print(f'Acurácia no conjunto de teste: {acuracy_test:.4f}')
    
    print(classification_report(dataset.y_test, y_pred_test))
    
   
