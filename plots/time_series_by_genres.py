from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

# Movies: genres divisions over time
df_movies = pd.read_sql('''
SELECT N.ListedIn AS Genre, N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie'
GROUP BY N.ListedIn, N.ReleaseYear;
''', engine)

df_movies.Genre = pd.Series([x.split(',') for x in df_movies.Genre])
df_movies = df_movies.explode('Genre')
df_movies['Genre'] = df_movies['Genre'].apply(lambda x: x.strip())
df_movies = df_movies.groupby(['Genre', 'ReleaseYear']).sum()
df_movies.reset_index(inplace=True)
df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
fig1 = px.scatter(df_movies, x='ReleaseYear', y='FemaleRatio', facet_col='Genre', facet_col_wrap=4)
fig1.write_html('results/time_series_by_genre_movies.html')


# TV Shows: genres divisions over time
df_tvshows = pd.read_sql('''
SELECT N.ListedIn AS Genre, N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='TV Show'
GROUP BY N.ListedIn, N.ReleaseYear;
''', engine)

df_tvshows.Genre = pd.Series([x.split(',') for x in df_tvshows.Genre])
df_tvshows = df_tvshows.explode('Genre')
df_tvshows['Genre'] = df_tvshows['Genre'].apply(lambda x: x.strip())
df_tvshows = df_tvshows.groupby(['Genre', 'ReleaseYear']).sum()
df_tvshows.reset_index(inplace=True)
df_tvshows['FemaleRatio'] = df_tvshows['FemaleCount']/(df_tvshows['MaleCount']+df_tvshows['FemaleCount'])
fig2 = px.scatter(df_tvshows, x='ReleaseYear', y='FemaleRatio', facet_col='Genre', facet_col_wrap=4)
fig2.write_html('results/time_series_by_genre_tvshows.html')