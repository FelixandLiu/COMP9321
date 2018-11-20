import pandas as pd
import matplotlib.pyplot as plt

def print_dataframe(dataframe, print_column=True, print_rows=True,):
    if print_column:
        print(",".join([column for column in dataframe]))
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))
def question_1():
    print('Question 1: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.reset_index(level=0, inplace=True)
    print_dataframe(merged_dataset.head(5))


def question_2():
    print('Question 2: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.reset_index(level=0, inplace=True)
    print_dataframe(merged_dataset.head(1))


def question_3():
    print('Question 3: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.reset_index(level=0, inplace=True)
    print_dataframe(merged_dataset.head())


def question_4():
    print('Question 4: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset.reset_index(level=0, inplace=True)
    print_dataframe(merged_dataset.tail(10))


def question_5():
    print('Question 5: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset['Gold_x'] = merged_dataset['Gold_x'].str.replace(",", "").astype(int)
    print(merged_dataset['Gold_x'][:-1].idxmax())

def question_6():
    print('Question 6: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset['Gold_x'] = merged_dataset['Gold_x'].str.replace(",", "").astype(int)
    merged_dataset['Gold_y'] = merged_dataset['Gold_y'].str.replace(",", "").astype(int)
    print((merged_dataset['Gold_x'][:-1]-merged_dataset['Gold_y'][:-1]).abs().idxmax())

def question_7():
    print('Question 7: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset['Gold_x'] = merged_dataset['Gold_x'].str.replace(",", "").astype(int)
    merged_dataset['Gold_y'] = merged_dataset['Gold_y'].str.replace(",", "").astype(int)
    merged_dataset['Total.1'] = merged_dataset['Total.1'].str.replace(",", "").astype(int)
    merged_dataset.drop(index='Totals',inplace=True)
    merged_dataset.sort_values(by=['Total.1'], ascending=False, inplace=True)
    merged_dataset.reset_index(level=0, inplace=True)
    print_dataframe(merged_dataset.head())
    print_dataframe(merged_dataset.tail())

def question_8():
    print('Question 8: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset['Gold_x'] = merged_dataset['Gold_x'].str.replace(",", "").astype(int)
    merged_dataset['Gold_y'] = merged_dataset['Gold_y'].str.replace(",", "").astype(int)
    merged_dataset['Total.1'] = merged_dataset['Total.1'].str.replace(",", "").astype(int)
    merged_dataset.drop(index='Totals', inplace=True)
    merged_dataset.sort_values(by=['Total.1'], ascending=False, inplace=True)
    merged_dataset['Total_x'] = merged_dataset['Total_x'].str.replace(",", "").astype(int)
    merged_dataset['Total_y'] = merged_dataset['Total_y'].str.replace(",", "").astype(int)
    merged_dataset.head(10)[['Total_y','Total_x']].plot(kind='barh',
                                                        stacked=True,
                                                        title='Medals for Winter and Summer Games').legend(['Winter games','Summer games'],
                                                        bbox_to_anchor=(0.5, -0.05),loc='upper center', ncol=2)
    plt.show()

def question_9():
    print('Question 9: ')
    dataset_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1, dtype={})
    dataset_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    merged_dataset = pd.merge(left=dataset_1, right=dataset_2, on=None, left_index=True, right_index=True)
    merged_dataset.index.name = 'Country name'
    merged_dataset.drop(columns='Rubish', inplace=True)
    merged_dataset.dropna(axis=0, how='all', inplace=True)
    merged_dataset['Gold_x'] = merged_dataset['Gold_x'].str.replace(",", "").astype(int)
    merged_dataset['Gold_y'] = merged_dataset['Gold_y'].str.replace(",", "").astype(int)
    merged_dataset['Total.1'] = merged_dataset['Total.1'].str.replace(",", "").astype(int)
    merged_dataset.drop(index='Totals', inplace=True)
    merged_dataset.sort_values(by=['Total.1'], ascending=False, inplace=True)
    merged_dataset['Total_x'] = merged_dataset['Total_x'].str.replace(",", "").astype(int)
    merged_dataset['Total_y'] = merged_dataset['Total_y'].str.replace(",", "").astype(int)
    merged_dataset['Silver_y'] = merged_dataset['Silver_y'].str.replace(",", "").astype(int)
    merged_dataset['Bronze_y'] = merged_dataset['Bronze_y'].str.replace(",", "").astype(int)
    merged_dataset.loc[[' United States (USA) [P] [Q] [R] [Z]',' Australia (AUS) [AUS] [Z]',' Great Britain (GBR) [GBR] [Z]',
                        ' Japan (JPN)',' New Zealand (NZL) [NZL]'],['Gold_y','Silver_y','Bronze_y']].plot(kind='bar',
                        title='Winter Games', rot=0).legend(['Winter games','Summer games'],
                        bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=2)
    plt.show()





if __name__ == '__main__':
    question_1()
    question_2()
    question_3()
    question_4()
    question_5()
    question_6()
    question_7()
    question_8()
    question_9()

