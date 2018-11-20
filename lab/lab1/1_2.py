import pandas as pd
import sqlite3
from pandas.io import sql
def load_csv(csv_file):
    df = pd.read_csv(csv_file)
    
def write_in_sql(dataframe, database_file,table_name):
    cnx = sqlite3.connect(database_file)
    sql.to_sql(dataframe,name=table_name,con=cnx)
#def query_database_and_reload():
if __name__=='__main__':
    csv_file='Demographic_Statistics_By_Zip_Code.csv'
    dataframe = load_csv(csv_file)
    sqll

    
