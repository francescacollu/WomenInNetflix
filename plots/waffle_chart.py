from matplotlib import table
import plotly.express as px
from chart_studio import plotly
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from pywaffle import Waffle

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

df['Error'] = df['UnspecifiedCount']+df['NameNotAvailable']
sum = df[['MaleCount', 'FemaleCount', 'Error']].sum()
df_general_counts = pd.DataFrame({'gender':['Male', 'Female', 'Error'], 'counts':sum})
s = df_general_counts['counts'].sum()
sm = list(df_general_counts.loc[df_general_counts['gender']=='Male','counts'])[0]
sf = list(df_general_counts.loc[df_general_counts['gender']=='Female','counts'])[0]
se = list(df_general_counts.loc[df_general_counts['gender']=='Error','counts'])[0]
df_percentage = pd.DataFrame({'gender':['Male', 'Female', 'Error'], 'percentage_counts':[math.floor((sm/s)*100), math.floor((sf/s)*100), math.ceil((se/s)*100)]})


data = {'Male':math.floor((sm/s)*1000), 'Female':math.ceil((sf/s)*1000), 'Error':math.floor((se/s)*1000)}
fig = plt.figure(
    FigureClass=Waffle, 
    rows=20, 
    values=data, 
    colors=("#636EFA", "#EF553B", "#00CC96"),
    #title={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
    labels=["{0} ({1}%)".format(k, v/10) for k, v in data.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(data), 'framealpha': 0}
)
fig.gca().set_facecolor('#EEEEEE')
fig.set_facecolor('#EEEEEE')
plt.savefig('results/whole_netflix_percentage.png', dpi='figure')


