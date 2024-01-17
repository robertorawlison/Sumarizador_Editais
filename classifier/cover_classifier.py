# -*- coding: utf-8 -*-

from .gpel_text_classifier import GpelTextClassifier

class CoverClassifier:
    def __init__(self):
        self.classifier = GpelTextClassifier()
        self.classifier.load()
        
    def isCover(self, text : str) -> bool:
        if self.classifier.predict(text) == +1:
            return True
        else:
            return False
        