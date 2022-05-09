from matplotlib import table
from numpy import size
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
import chart_studio.plotly as py
import chart_studio.tools as tls
from credential_file import *

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file

# Movies: time series
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_movies_time_series = pd.read_sql('''
SELECT N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable, COUNT(*) AS MoviesCount
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type = 'Movie' 
GROUP BY ReleaseYear;
''', engine)
# df_movies_time_series['Error'] = df_movies_time_series['UnspecifiedCount']+df_movies_time_series['NameNotAvailable']
# fig1 = px.scatter(df_movies_time_series, x='ReleaseYear', y=['MaleCount', 'FemaleCount'], error_y='Error')
# fig1.write_html('results/movies_time_series.html')
df_movies_time_series['Generic'] = df_movies_time_series['FemaleCount']/(df_movies_time_series['MaleCount']+df_movies_time_series['FemaleCount'])
# fig2 = px.scatter(df_movies_time_series, x='ReleaseYear', y=['Generic'])
# fig2.write_html('results/movies_time_series_percentage.html')

# Main characters in Movies
df_movies_time_series['Main'] = df_movies_time_series['MainFemale']/(df_movies_time_series['MainMale']+df_movies_time_series['MainFemale'])
df_movies_time_series = df_movies_time_series.melt(id_vars=['ReleaseYear', 'MoviesCount'], value_vars=['Generic', 'Main'], var_name='CharacterType', value_name='Ratio')
fig3 = px.scatter(df_movies_time_series, x='ReleaseYear', y='Ratio'
        , size='MoviesCount'
        , size_max=35
        , facet_col='CharacterType')
fig3.update_traces(marker=dict(color='#FF7F0E'))
fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig3.for_each_annotation(lambda a: a.update(x=0.06) if a.text=='Generic' else a.update(x=0.56))
fig3.for_each_annotation(lambda a: a.update(y=1.))
fig3.for_each_annotation(lambda a: a.update(font=dict(size=20, color='black')))
fig3.add_hline(y=0.5, annotation_text="50% ", line_dash="dot",annotation_position="top left", line=dict(color="rgb(204,204,204)",width=2), annotation_font_size=18, annotation_font_color="black")
fig3.for_each_annotation(lambda a: a.update(text='<b>'+a.text+'</b>'))
fig3.for_each_annotation(lambda a: a.update(opacity=0.3))
fig3.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', yaxis_title=None, title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, 
        showlegend=True)
fig3.update_xaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16, color='#7F7F7F'), title_font=dict(color='#7F7F7F', size=16))
fig3.update_yaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',
                  tickmode = 'array',
                  tickvals = [0., 0.2, 0.4, 0.6, 0.8, 1.],
                  ticktext = ['0%', '20%', '40%', '60%', '80%', '100%']
                  ,tickfont=dict(size=16,color='#7F7F7F'))
fig3.write_html('results/main_characters_movies_time_series_percentage.html')
py.plot(fig3, filename='main_characters_movies_time_series_percentage', auto_open = False) # Add plot on Plotly profile for embedding on Medium



# TV Shows: time series
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')

df_tvshows_time_series = pd.read_sql('''
SELECT N.ReleaseYear AS ReleaseYear, SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(NameNotAvailable) AS NameNotAvailable, SUM(G.MainMale) AS MainMale, SUM(G.MainFemale) AS MainFemale, SUM(G.MainUnspecified) AS MainUnspecified, SUM(MainNotAvailable) AS MainNotAvailable, COUNT(*) AS ShowsCount
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type = 'TV Show' 
GROUP BY ReleaseYear;
''', engine)
# df_tvshows_time_series['Error'] = df_tvshows_time_series['UnspecifiedCount']+df_tvshows_time_series['NameNotAvailable']
# fig4 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y=['MaleCount', 'FemaleCount'], error_y='Error')
# fig4.write_html('results/tvshows_time_series.html')

df_tvshows_time_series['Generic'] = df_tvshows_time_series['FemaleCount']/(df_tvshows_time_series['MaleCount']+df_tvshows_time_series['FemaleCount'])
# fig5 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y=['Generic'])
# fig5.write_html('results/tvshows_time_series_percentage.html')

# Main characters in TV Shows
df_tvshows_time_series['Main'] = df_tvshows_time_series['MainFemale']/(df_tvshows_time_series['MainMale']+df_tvshows_time_series['MainFemale'])
df_tvshows_time_series = df_tvshows_time_series.melt(id_vars=['ReleaseYear', 'ShowsCount'], value_vars=['Generic', 'Main'], var_name='CharacterType', value_name='Ratio')
fig6 = px.scatter(df_tvshows_time_series, x='ReleaseYear', y='Ratio'
        , size='ShowsCount'
        , size_max=35
        , facet_col='CharacterType')
fig6.update_traces(marker=dict(color='#FF7F0E'))
fig6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig6.for_each_annotation(lambda a: a.update(x=0.06) if a.text=='Generic' else a.update(x=0.56))
fig6.for_each_annotation(lambda a: a.update(y=1.))
fig6.for_each_annotation(lambda a: a.update(font=dict(size=20, color='black')))
fig6.add_hline(y=0.5, annotation_text="50% ", line_dash="dot",annotation_position="top left", line=dict(color="rgb(204,204,204)",width=2), annotation_font_size=18, annotation_font_color="black")
fig6.for_each_annotation(lambda a: a.update(text='<b>'+a.text+'</b>'))
fig6.for_each_annotation(lambda a: a.update(opacity=0.3))
fig6.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', yaxis_title=None, title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, 
        showlegend=True)
fig6.update_xaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16, color='#7F7F7F'), title_font=dict(color='#7F7F7F', size=16))
fig6.update_yaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',
                  tickmode = 'array',
                  tickvals = [0., 0.2, 0.4, 0.6, 0.8, 1.],
                  ticktext = ['0%', '20%', '40%', '60%', '80%', '100%']
                  ,tickfont=dict(size=16,color='#7F7F7F'))
fig6.write_html('results/main_characters_tvshows_time_series_percentage.html')
py.plot(fig6, filename='main_characters_tvshows_time_series_percentage', auto_open = False) # Add plot on Plotly profile for embedding on Medium
