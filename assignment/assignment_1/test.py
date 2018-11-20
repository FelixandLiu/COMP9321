# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 17:43:06 2018

@author: GFLiu
"""

import pandas as pd
import matplotlib.pyplot as plt
dataset_1 = pd.read_csv('Olympics_dataset1.csv',index_col=0,skiprows=1)
dataset_2 = pd.read_csv('Olympics_dataset2.csv',index_col=0,skiprows=1)
dataset_1['Country name'] = dataset_1['Country name'].str.strip()
print(dataset_1.loc[' United States (USA) [P] [Q] [R] [Z]'])
plt.show()
