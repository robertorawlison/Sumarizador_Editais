# -*- coding: utf-8 -*-
from datetime import datetime
import re
import locale

class Summarizer:
    def summarize(self, text : str) -> str:
        return ""

    def convert_to_datetime(self,date_str):
        
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        
        date_formats = [
            '%d de %B de %Y',  # 01 de Janeiro de 2023
            '%d/%m/%Y',         # 01/01/2023
        ]

        for date_format in date_formats:
            try:
                date_object = datetime.strptime(date_str, date_format)
                return date_object
            except ValueError:
                pass

        return datetime.max

    def _encontra_data(self, text : str) -> datetime:
        a = r'^.*\s*[.,]\s*([0-9]{2}\s*(?:de\s*)?(?:(?:J|j)aneiro|(?:F|f)evereiro|(?:M|m)ar(?:ç|c)o|(?:A|a)bril|(?:M|m)aio|(?:J|j)unho|(?:J|j)ulho|(?:A|a)gosto|(?:S|s)etembro|(?:O|o)utubro|(?:N|n)ovembro|(?:D|d)ezembro)\s*(?:de\s*)?[0-9]{4})'
        b = r'^.*[A-Z]{2}\s*[.,]\s*([0-9]{2}\s*(?:de\s*)?(?:(?:J|j)aneiro|(?:F|f)evereiro|(?:M|m)ar(?:ç|c)o|(?:A|a)bril|(?:M|m)aio|(?:J|j)unho|(?:J|j)ulho|(?:A|a)gosto|(?:S|s)etembro|(?:O|o)utubro|(?:N|n)ovembro|(?:D|d)ezembro)\s*(?:de\s*)?[0-9]{4})'
        c = r'^.*[A-Z]{2}\s*[.,]\s*([0-9]{2}\s*/[0-9]{2}\s*/[0-9]{4}\s*)'
        d = r'^.*\s*[.,]\s*em\s*([0-9]{2}\s*(?:de\s*)?(?:(?:J|j)aneiro|(?:F|f)evereiro|(?:M|m)ar(?:ç|c)o|(?:A|a)bril|(?:M|m)aio|(?:J|j)unho|(?:J|j)ulho|(?:A|a)gosto|(?:S|s)etembro|(?:O|o)utubro|(?:N|n)ovembro|(?:D|d)ezembro)\s*(?:de\s*)?[0-9]{4})'

        aparicoes_a = re.findall(a, text, re.IGNORECASE|re.MULTILINE)
        aparicoes_b = re.findall(b, text, re.MULTILINE)
        aparicoes_c = re.findall(c, text, re.MULTILINE)
        aparicoes_d = re.findall(d, text, re.IGNORECASE|re.MULTILINE)

        if aparicoes_b:
            #print("estado")
            return self.convert_to_datetime(aparicoes_b[0])
        elif aparicoes_a:
            #print("qq coisa")
            return self.convert_to_datetime(aparicoes_a[0])
        elif aparicoes_c:
            #print("barra")
            return self.convert_to_datetime(aparicoes_c[0])
        elif aparicoes_d:
            #print("em")
            return self.convert_to_datetime(aparicoes_d[0])
        else:
            return datetime.max

