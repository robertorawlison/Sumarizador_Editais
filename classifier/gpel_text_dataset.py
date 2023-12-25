# -*- coding: utf-8 -*-



class GpelTextDataset
    '''
    Classe que manipula os dados de texto do datset GPEL
    '''
    def __init__(self):
        pass
    
    def load(self) -> None:
        '''
        Carrega todos os arquivos de texto (.txt) do dataset GPEL
        e adiciona na matriz de textos X associando o mesmo ao rótulo
        y. Se o texto estiver no diretório cover será rotulado com +1,
        se estiver no rótulo non-cover será rotulado com -1
        Returns
        -------
        None.

        '''
        pass
    
    def preprocessing(self) - > None:
        '''
        Tratamento de PLN sobre os textos:
            1. Lenatização das plavras;
            2. Remoção dos acentos (minimiza erros do OCR);
            3. Remoção das stop words (lenatizadas e sem acento);
            4. Remoção das palavras frequentes no vocabulário. Para a remoção
            de termos frequentes existem duas possibilidades:
                4.1 Experiemntal. Determinar qual limiar de frequência mínima
                produz os melhores resultados em instâncias de teste ou validação;
                4.2 TF-IDF (Term Frequency-Inverse Document Frequency), que 
                levam em conta a importância relativa de uma palavra em 
                relação ao documento e ao corpus.
        
        A matriz X resultante é uma lista de textos tratados, onde cada 
        texto é uma lista de strings
        X=[['três', 'dois', 'apoio', 'sobre', 'algo'],
           ['querer', 'tende', 'dezanove', 'eles']
            ]

        Returns
        -------
        None.

        '''
        pass


    def 