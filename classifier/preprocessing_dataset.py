# -*- coding: utf-8 -*-
from gpel_text_dataset import GpelTextDataset

if __name__ == "__main__":
    dataset = GpelTextDataset()
    dataset.preprocessing(0.25)
    dataset.save_train_test()
    
    