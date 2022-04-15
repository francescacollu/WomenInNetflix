from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

def RetrieveDataframe(password, db_name, table_name):
    engine = create_engine('mysql+mysqlconnector://root:'+password+'@127.0.0.1:3306/'+db_name)
    df = pd.read_sql('''
    SELECT *
    FROM '''+table_name+''';
    ''', engine)
    return df

df_genders_count = RetrieveDataframe('12345678', 'women_in_netflix', 'GendersCount')
df_netflix = RetrieveDataframe('12345678', 'women_in_netflix', 'Netflix')

df = df_genders_count.merge(df_netflix, how='left', on=['ShowId'])

# Whole catalog
df['Error'] = df['UnspecifiedCount']+df['NameNotAvailable']
sum = df[['MaleCount', 'FemaleCount', 'Error']].sum()
df_general_counts = pd.DataFrame({'gender':['Male', 'Female', 'Error'], 'counts':sum})
fig1 = px.bar(df_general_counts, x='gender', y='counts')
fig1.write_html('results/whole_netflix.html')

df['MainError'] = df['MainUnspecified']+df['MainNotAvailable']
main_characters_sum = df[['MainMale', 'MainFemale', 'MainError']].sum()
df_main_characters = pd.DataFrame({'gender':['MainMale', 'MainFemale', 'MainError'], 'counts':main_characters_sum})
fig2 = px.bar(df_main_characters, x='gender', y='counts')
fig2.write_html('results/main_characters_whole_netflix.html')