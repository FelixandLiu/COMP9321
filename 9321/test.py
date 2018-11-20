import pandas as pd

dataset_1 = pd.read_csv('Olympics_dataset1.csv',index_col=0,skiprows=1)
dataset_2 = pd.read_csv('Olympics_dataset2.csv',index_col=0,skiprows=1)


which_country=pivot_table(dataset_1,value='Gold_x',index='Country name',aggfunc=np.max)
print(dataset_1.tail())
