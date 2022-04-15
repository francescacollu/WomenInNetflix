from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

# Movies: Countrys divisions over time
df_movies = pd.read_sql('''
SELECT N.Country AS Country, N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, 
	SUM(UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie' AND N.Country IS NOT NULL
GROUP BY N.Country, N.ReleaseYear;
''', engine)

df_movies.Country = pd.Series([x.split(',') for x in df_movies.Country])
df_movies = df_movies.explode('Country')
df_movies['Country'] = df_movies['Country'].apply(lambda x: x.strip())
df_movies = df_movies.groupby(['Country', 'ReleaseYear']).sum()
df_movies.reset_index(inplace=True)
df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
fig1 = px.scatter(df_movies, x='ReleaseYear', y='FemaleRatio', color='Country')#, facet_col='Country', facet_col_wrap=4)
fig1.write_html('results/time_series_by_country_movies.html')