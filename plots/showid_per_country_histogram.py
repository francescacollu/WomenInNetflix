from matplotlib import table
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

# Movies
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_movies_per_year = pd.read_sql('''
SELECT Country, ShowId
FROM Netflix
WHERE Type = 'Movie';
''', engine)

fig = px.histogram(df_movies_per_year, x=['Country'])

fig.update_layout(plot_bgcolor='rgb(255,255,255)')
fig.write_html('results/movies_per_country_histogram.html')


# TV Shows
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_movies_per_year = pd.read_sql('''
SELECT Country, ShowId
FROM Netflix
WHERE Type = 'TV Show';
''', engine)

fig = px.histogram(df_movies_per_year, x=['Country'])

fig.update_layout(plot_bgcolor='rgb(255,255,255)')
fig.write_html('results/tvshows_per_country_histogram.html')