import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from plotly.graph_objs import *
import chart_studio.plotly as py

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df = pd.read_sql('''
SELECT N.Type, SUM(G.DirectorsMaleCount) AS Male, SUM(G.DirectorsFemaleCount) AS Female, SUM(G.DirectorsUnspecifiedCount) AS UnspecifiedCount, SUM(G.DirectorsNameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
GROUP BY N.Type;
''', engine)

df_null = pd.read_sql('''
SELECT Type, COUNT(*) AS NullCount
FROM Netflix
WHERE Director IS NULL
GROUP BY Type;
''', engine)
df = df.merge(df_null, on=['Type'])

df['Error'] = df['UnspecifiedCount']+df['NameNotAvailable']

fig = px.histogram(df, x='Type', y=['Male', 'Female', 'Error', 'NullCount'], barmode='group')
fig.update_layout(plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(visible=False)
fig.write_html('results/directors_type.html')