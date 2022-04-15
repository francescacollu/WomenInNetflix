from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd


# Movies: production country divisions
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

df_movies = pd.read_sql('''
SELECT N.Country AS Country, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie' AND N.Country IS NOT NULL
GROUP BY N.Country;
''', engine)

df_movies.Country = pd.Series([x.split(',') for x in df_movies.Country])
df_movies = df_movies.explode('Country')
df_movies['Country'] = df_movies['Country'].apply(lambda x: x.strip())
df_movies = df_movies.groupby(['Country']).sum()
df_movies.reset_index(inplace=True)

df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['MainFemaleRatio'] = df_movies['MainFemale']/(df_movies['MainMale']+df_movies['MainFemale'])
fig2 = px.bar(df_movies, x='Country', y=['FemaleRatio'])
fig2.update_layout(xaxis={'categoryorder':'total ascending'})
fig2.write_html('results/movies_country_division_percentage.html')


# TV Shows: production country divisions
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

df_tvshows = pd.read_sql('''
SELECT N.Country AS Country, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='TV Show' AND N.Country IS NOT NULL
GROUP BY N.Country;
''', engine)

df_tvshows.Country = pd.Series([x.split(',') for x in df_tvshows.Country])
df_tvshows = df_tvshows.explode('Country')
df_tvshows['Country'] = df_tvshows['Country'].apply(lambda x: x.strip())
df_tvshows = df_tvshows.groupby(['Country']).sum()
df_tvshows.reset_index(inplace=True)

df_tvshows['FemaleRatio'] = df_tvshows['FemaleCount']/(df_tvshows['MaleCount']+df_tvshows['FemaleCount'])
df_tvshows['MainFemaleRatio'] = df_tvshows['MainFemale']/(df_tvshows['MainMale']+df_tvshows['MainFemale'])
fig2 = px.bar(df_tvshows, x='Country', y=['FemaleRatio'])
fig2.update_layout(xaxis={'categoryorder':'total ascending'})
fig2.write_html('results/tvshows_country_division_percentage.html')
