import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from plotly.graph_objs import *
import chart_studio.plotly as py
import chart_studio.tools as tls
from credential_file import *

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file

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

# Genre division
df_movies = pd.read_sql('''
SELECT N.ListedIn AS Genre, SUM(G.DirectorsMaleCount) AS MaleCount, SUM(G.DirectorsFemaleCount) AS FemaleCount
FROM Netflix N INNER JOIN GendersCount G ON N.ShowId=G.ShowId
WHERE N.Type='Movie'
GROUP BY N.ListedIn;
''', engine)

df_movies.Genre = pd.Series([x.split(',') for x in df_movies.Genre])
df_movies = df_movies.explode('Genre')
df_movies['Genre'] = df_movies['Genre'].apply(lambda x: x.strip())
df_movies = df_movies.groupby(['Genre']).sum()
df_movies.reset_index(inplace=True)

df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['FemaleRatioPercentage'] = round(df_movies['FemaleRatio']*100, 1)
df_movies['FemaleRatioPercentage'] = df_movies['FemaleRatioPercentage'].astype(str)+'%'
fig2 = px.bar(df_movies, y='Genre', x=['FemaleRatio'], orientation='h', text='FemaleRatioPercentage', barmode='group')#, title='Female Directors Presence Percentage Distribution over Movie Genres')
fig2.update_traces(marker_color='rgb(56, 166, 165)')
fig2.add_vline(x=0.5, annotation_text="50% ", line_dash="dot",annotation_position="bottom right", line=dict(color="rgb(204,204,204)",width=4), annotation_font_size=18, annotation_font_color="black")
fig2.for_each_annotation(lambda a: a.update(text='<b>'+a.text+'</b>'))
fig2.for_each_annotation(lambda a: a.update(opacity=0.3))
fig2.update_yaxes(tickfont=dict(size=16,color='black'))
fig2.update_traces(textfont_size=15)
fig2.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', xaxis_visible=False, yaxis_title=None, title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
        ,width=1100
        ,height=700
        ,showlegend=False)
fig2.write_html('results/directors_movies_genres_division_percentage.html')
py.plot(fig2, filename='directors_movies_genres_division', auto_open = False)

# Time series
df_time_series = pd.read_sql('''
SELECT N.ReleaseYear AS ReleaseYear, SUM(G.DirectorsMaleCount) AS MaleCount, SUM(G.DirectorsFemaleCount) AS FemaleCount, COUNT(*) AS MoviesCount
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type = 'Movie' 
GROUP BY ReleaseYear;
''', engine)
df_time_series['Ratio'] = df_time_series['FemaleCount']/(df_time_series['MaleCount']+df_time_series['FemaleCount'])

fig3 = px.scatter(df_time_series, x='ReleaseYear', y='Ratio'
        , size='MoviesCount'
        , size_max=35)
        #, title='<b>Women Movie Directors Ratio</b>')
fig3.update_traces(marker=dict(color='rgb(56, 166, 165)'))
fig3.add_hline(y=0.5, annotation_text="50% ", line_dash="dot",annotation_position="bottom right", line=dict(color="rgb(204,204,204)",width=2), annotation_font_size=18, annotation_font_color="black")
fig3.for_each_annotation(lambda a: a.update(text='<b>'+a.text+'</b>'))
fig3.for_each_annotation(lambda a: a.update(opacity=0.3))
fig3.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', yaxis_title=None, title={
        'y':0.88,
        'x':0.05,
        'xanchor': 'left',
        'yanchor': 'top'}, 
        showlegend=True)
fig3.add_annotation(x=0.01, y=1.1, xref='paper', yref='paper', text='<b>Women Movie Directors Ratio</b>', opacity=0.5, showarrow=False, font=dict(size=18, color='black'))
fig3.update_xaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16, color='#7F7F7F'), title_font=dict(color='#7F7F7F', size=16))
fig3.update_yaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',
                  tickmode = 'array',
                  tickvals = [0., 0.2, 0.4, 0.6, 0.8, 1.],
                  ticktext = ['0%', '20%', '40%', '60%', '80%', '100%']
                  ,tickfont=dict(size=16,color='#7F7F7F'))
fig3.write_html('results/directors_time_series.html')
py.plot(fig3, filename='directors_time_series', auto_open = False)