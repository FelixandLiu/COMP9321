import pandas as pd
import numpy as np
df = pd.read_csv('Demographic_Statistics_By_Zip_Code.csv')
print(df)
colum_header=list(df.columns.values)
print(colum_header)
'''
for index, row in df.iterrows():
    for e in colum_header:
        print(row[e],end='  ')
    print('\n')
'''
df.to_csv('lab1_1.csv')
    
