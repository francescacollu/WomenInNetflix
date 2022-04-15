from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

# Movies: time series
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_movies_time_series = pd.read_sql('''
SELECT N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type = 'Movie' 
GROUP BY ReleaseYear;
''', engine)
df_movies_time_series['Error'] = df_movies_time_series['UnspecifiedCount']+df_movies_time_series['NameNotAvailable']
fig1 = px.scatter(df_movies_time_series, x='ReleaseYear', y=['MaleCount', 'FemaleCount'], error_y='Error')
fig1.write_html('results/movies_time_series.html')
df_movies_time_series['FemaleRatio'] = df_movies_time_series['FemaleCount']/(df_movies_time_series['MaleCount']+df_movies_time_series['FemaleCount'])
fig2 = px.scatter(df_movies_time_series, x='ReleaseYear', y=['FemaleRatio'])
fig2.write_html('results/movies_time_series_percentage.html')

# Main characters in Movies
df_movies_time_series['MainFemaleRatio'] = df_movies_time_series['MainFemale']/(df_movies_time_series['MainMale']+df_movies_time_series['MainFemale'])
fig3 = px.scatter(df_movies_time_series, x='ReleaseYear', y=['MainFemaleRatio', 'FemaleRatio'])
fig3.write_html('results/main_characters_movies_time_series_percentage.html')


# TV Shows: time series
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

df_tvshows_time_series = pd.read_sql('''
SELECT N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type = 'TV Show' 
GROUP BY ReleaseYear;
''', engine)
df_tvshows_time_series['Error'] = df_tvshows_time_series['UnspecifiedCount']+df_tvshows_time_series['NameNotAvailable']
fig4 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y=['MaleCount', 'FemaleCount'], error_y='Error')
fig4.write_html('results/tvshows_time_series.html')

df_tvshows_time_series['FemaleRatio'] = df_tvshows_time_series['FemaleCount']/(df_tvshows_time_series['MaleCount']+df_tvshows_time_series['FemaleCount'])
fig5 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y=['FemaleRatio'])
fig5.write_html('results/tvshows_time_series_percentage.html')

# Main characters in TV Shows
df_tvshows_time_series['MainFemaleRatio'] = df_tvshows_time_series['MainFemale']/(df_tvshows_time_series['MainMale']+df_tvshows_time_series['MainFemale'])
fig6 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y=['MainFemaleRatio','FemaleRatio'])
fig6.write_html('results/main_characters_tvshows_time_series_percentage.html')