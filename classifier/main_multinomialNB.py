# -*- coding: utf-8 -*-
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

from gpel_text_dataset import GpelTextDataset

if __name__ == "__main__":
    dataset = GpelTextDataset(0.25)
   
    mnb = MultinomialNB()
    mnb.fit(dataset.X_train, dataset.y_train)
    
    y_prob = mnb.predict_proba(dataset.X_test)
    print(y_prob)
    y_pred = mnb.predict(dataset.X_test)
    #print(y_pred)
    
    print(classification_report(dataset.y_test, y_pred))

