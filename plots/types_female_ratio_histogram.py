from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from plotly.graph_objs import *
import chart_studio.plotly as py

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_movies = pd.read_sql('''
SELECT G.MaleCount AS MaleCount, G.FemaleCount AS FemaleCount, 
	UnspecifiedCount AS UnspecifiedCount, NameNotAvailable AS NameNotAvailable, G.MainMale AS MainMale, G.MainFemale AS MainFemale, G.MainUnspecified AS MainUnspecified, MainNotAvailable AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie';
''', engine)

df_movies['Error'] = df_movies['UnspecifiedCount']+df_movies['NameNotAvailable']
df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['MainFemaleRatio'] = df_movies['MainFemale']/(df_movies['MainMale']+df_movies['MainFemale'])
df_movies['MaleRatio'] = df_movies['MaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['MainMaleRatio'] = df_movies['MainMale']/(df_movies['MainMale']+df_movies['MainFemale'])
fig = px.histogram(df_movies, x=['FemaleRatio'], nbins=10)
fig.update_layout(plot_bgcolor='rgb(255,255,255)')
fig.write_html('results/movie_female_ratio.html')

fig2 = px.histogram(df_movies, x=['MainFemaleRatio'])
fig2.update_layout(plot_bgcolor='rgb(255,255,255)')
fig2.write_html('results/movie_mainfemale_ratio.html')

fig3 = px.histogram(df_movies, x=['MaleRatio'], nbins=10)
fig3.update_layout(plot_bgcolor='rgb(255,255,255)')
fig3.write_html('results/movie_male_ratio.html')

fig4 = px.histogram(df_movies, x=['MainMaleRatio'])
fig4.update_layout(plot_bgcolor='rgb(255,255,255)')
fig4.write_html('results/movie_mainmale_ratio.html')