# -*- coding: utf-8 -*-
import re
from datetime import datetime
from .summarizer import Summarizer

class AditivoSummarizer(Summarizer):
    def summarize(self, text : str) -> str:
        summary = " "
        date = datetime.now()
        return (summary, date) 
