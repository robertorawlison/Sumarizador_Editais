# -*- coding: utf-8 -*-
from classifier import GpelTextDataset

if __name__ == "__main__":
    dataset = GpelTextDataset()
    dataset.preprocessing()
    #dataset.save_preprocessing()
    
    