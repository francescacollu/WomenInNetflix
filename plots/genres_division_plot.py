from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd


# Movies: genres divisions
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

df_movies = pd.read_sql('''
SELECT N.ListedIn AS Genre, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie'
GROUP BY N.ListedIn;
''', engine)

df_movies.Genre = pd.Series([x.split(',') for x in df_movies.Genre])
df_movies = df_movies.explode('Genre')
df_movies['Genre'] = df_movies['Genre'].apply(lambda x: x.strip())
df_movies = df_movies.groupby(['Genre']).sum()
df_movies.reset_index(inplace=True)

fig1 = px.bar(df_movies, y='Genre', x=['MaleCount', 'FemaleCount', 'UnspecifiedCount', 'NameNotAvailable'], orientation='h')
fig1.write_html('results/movies_genres_division.html')

df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['MainFemaleRatio'] = df_movies['MainFemale']/(df_movies['MainMale']+df_movies['MainFemale'])
fig2 = px.bar(df_movies, y='Genre', x=['FemaleRatio'], orientation='h')
fig2.update_layout(yaxis={'categoryorder':'total ascending'})
fig2.write_html('results/movies_genres_division_percentage.html')

fig2_main = px.bar(df_movies, y='Genre', x=['MainFemaleRatio'], orientation='h')
fig2_main.update_layout(yaxis={'categoryorder':'total ascending'})
fig2_main.write_html('results/movies_genres_division_percentage_main.html')


# TV Shows
df_tvshows = pd.read_sql('''
SELECT N.ListedIn AS Genre, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='TV Show'
GROUP BY N.ListedIn;
''', engine)

df_tvshows.Genre = pd.Series([x.split(',') for x in df_tvshows.Genre])
df_tvshows = df_tvshows.explode('Genre')
df_tvshows['Genre'] = df_tvshows['Genre'].apply(lambda x: x.strip())
df_tvshows = df_tvshows.groupby(['Genre']).sum()
df_tvshows.reset_index(inplace=True)

fig3 = px.bar(df_tvshows, y='Genre', x=['MaleCount', 'FemaleCount', 'UnspecifiedCount', 'NameNotAvailable'], orientation='h')
fig3.write_html('results/tvshows_genres_division.html')

df_tvshows['FemaleRatio'] = df_tvshows['FemaleCount']/(df_tvshows['MaleCount']+df_tvshows['FemaleCount'])
df_tvshows['MainFemaleRatio'] = df_tvshows['MainFemale']/(df_tvshows['MainMale']+df_tvshows['MainFemale'])
fig4 = px.bar(df_tvshows, y='Genre', x=['FemaleRatio'], orientation='h')
fig4.update_layout(yaxis={'categoryorder':'total ascending'})
fig4.write_html('results/tvshows_genres_division_percentage.html')

fig4_main = px.bar(df_tvshows, y='Genre', x=['MainFemaleRatio'], orientation='h')
fig4_main.update_layout(yaxis={'categoryorder':'total ascending'})
fig4_main.write_html('results/tvshows_genres_division_percentage_main.html')