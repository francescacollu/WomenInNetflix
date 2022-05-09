from matplotlib.pyplot import text
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
import chart_studio.plotly as py
import chart_studio.tools as tls
import plotly.graph_objects as go
import numpy as np

username='fcollu'
api_key='KlCMv4upeJgOV69aFpmr'
tls.set_credentials_file(username=username,
                                        api_key=api_key)

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

df_movies['FemaleRatio'] = df_movies['FemaleCount']/(df_movies['MaleCount']+df_movies['FemaleCount'])
df_movies['Generic'] = round(df_movies['FemaleRatio']*100, 2)
df_movies['MainFemaleRatio'] = df_movies['MainFemale']/(df_movies['MainMale']+df_movies['MainFemale'])
df_movies['Main'] = round(df_movies['MainFemaleRatio']*100, 2)
fig2 = px.bar(df_movies, y='Genre', x=['Generic', 'Main'] 
			  ,orientation='h'
			  ,text_auto='.2f' 
			  ,barmode='group' 
			  ,color_discrete_map={'Generic':'#FF7F0E', 'Main':'#D62728'}
			  ,labels={'Generic': 'General character', 'Main': 'Main character'})
fig2.for_each_trace(lambda t: t.update(texttemplate = t.texttemplate + ' %'))
fig2.update_traces(textfont_size=18, textposition="outside", cliponaxis=False)
fig2.update_layout(yaxis={'categoryorder':'total descending'}
				   ,plot_bgcolor='white'
				   ,xaxis_visible=False
				   ,yaxis_title=None
				   ,legend_title_text=None
				   ,legend=dict(
					     orientation = 'h'
    					,yanchor="top"
    					,y=1.05
    					,xanchor="center"
    					,x=1.)
				   ,title={
						'y':0.9,
						'x':0.5,
						'xanchor': 'center',
						'yanchor': 'top'}
				   ,autosize=False
			       ,width=1000
    			   ,height=700)
fig2.write_html('results/movies_genres_division_percentage.html')

# Add plot on Plotly profile for embedding on Medium
# py.plot(fig2, filename='movies_genres_division', auto_open = False)

df_movies = df_movies.melt(id_vars=['Genre'], value_vars=['Generic', 'Main'], var_name='CharacterType', value_name='Ratio')
fig = px.line(df_movies, y="Ratio", x="CharacterType", color="Genre", markers=True)
fig.update_traces(marker=dict(size=15), line=dict(color='rgb(204, 80, 62)'))
genres = list(df_movies.Genre.unique())
negative_slope_genres = [g for g in genres if list(df_movies[(df_movies['Genre']==g)&(df_movies['CharacterType']=='Main')]['Ratio'])[0]-list(df_movies[(df_movies['Genre']==g)&(df_movies['CharacterType']=='Generic')]['Ratio'])[0] < 0]
fig.for_each_trace(
	lambda trace: trace.update(line=dict(color='rgb(56, 166, 165)')) if trace.name in negative_slope_genres else (),
)
labels_font_size=15
for g in genres:
	y0 = list(df_movies[(df_movies['Genre']==g)&(df_movies['CharacterType']=='Main')]['Ratio'])[0]
	if g == 'Independent Movies':
		dy = 0.9
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Dramas':
		dy = 0.9
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Thrillers':
		dy = 0.7
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Comedies':
		dy = -0.7
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Documentaries':
		dy = 0.4
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Stand-Up Comedy':
		dy = -0.4
		fig.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	else:
		fig.add_annotation(x=1.4, y=y0, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=220)
		fig.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0, line_color='black', xref='x', yref='y', layer='below', line_width=1)
for g in genres:
	y0 = list(df_movies[(df_movies['Genre']==g)&(df_movies['CharacterType']=='Generic')]['Ratio'])[0]
	if g == 'LGBTQ Movies':
		dy = 0.4
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Romantic Movies':
		dy = -0.4
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Independent Movies':
		dy = 1.3
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Comedies':
		dy = 1
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Dramas':
		dy = 0.65
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'International Movies':
		dy = 0.2
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Faith & Spirituality':
		dy = -0.4
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Thrillers':
		dy = -0.8
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Music & Musicals':
		dy = -1.2
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Classic Movies':
		dy = 0.8
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Sports Movies':
		dy = 0.3
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Cult Movies':
		dy = -0.4
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Action & Adventure':
		dy = -0.6
		fig.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	else:
		fig.add_annotation(x=-0.4, y=y0, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=220)
		fig.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0, line_color='black', xref='x', yref='y', layer='below', line_width=1)

# Background
for y in np.arange(18, 60, 1):
	if y%5 != 0:
		fig.add_shape(type='line', x0=0.05, x1=0.95, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
	else:
		fig.add_shape(type='line', x0=0.05, x1=0.37, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
		fig.add_shape(type='line', x0=0.63, x1=0.95, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
for y in np.arange(20, 60, 5):
	fig.add_annotation(x=0.5, y=y, text=str(y)+'%', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig.add_annotation(x=-0.4, y=16, text='<b>Generic<br>Characters</b>', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig.add_annotation(x=1.4, y=16, text='<b>Main<br>Characters</b>', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig.update_layout(plot_bgcolor='white'
				   ,xaxis_title=None
				   ,yaxis_title=None
				   ,yaxis_visible=False
				   ,xaxis_visible=False
				   ,width=1000
				   ,height=850
				   ,showlegend=False)
fig.write_html('results/slope_chart_movies_genres_general_vs_main.html')
# Add plot on Plotly profile for embedding on Medium
py.plot(fig, filename='slope_movies_genres_division', auto_open = False)

################################
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
df_tvshows = df_tvshows[df_tvshows['Genre']!='TV Shows']
df_tvshows = df_tvshows.groupby(['Genre']).sum()
df_tvshows.reset_index(inplace=True)

df_tvshows['FemaleRatio'] = df_tvshows['FemaleCount']/(df_tvshows['MaleCount']+df_tvshows['FemaleCount'])
df_tvshows['Generic'] = round(df_tvshows['FemaleRatio']*100, 2)
df_tvshows['MainFemaleRatio'] = df_tvshows['MainFemale']/(df_tvshows['MainMale']+df_tvshows['MainFemale'])
df_tvshows['Main'] = round(df_tvshows['MainFemaleRatio']*100, 2)
fig4 = px.bar(df_tvshows, x='Genre', y=['Generic', 'Main'], orientation='v', text_auto='.2f',
barmode='group', color_discrete_map={'Generic':'#FF7F0E', 'Main':'#D62728'}, title='Actresses Presence Percentage Distribution over TV-Show Genres')
fig4.for_each_trace(lambda t: t.update(texttemplate = t.texttemplate + ' %'))
fig4.update_layout(xaxis={'categoryorder':'total descending'}, plot_bgcolor='white', yaxis_visible=False, xaxis_title=None, legend_title_text='General vs Main Characters', title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig4.write_html('results/tvshows_genres_division_percentage.html')
# py.plot(fig4, filename='tvshows_genres_division', auto_open = False)

df_tvshows = df_tvshows.melt(id_vars=['Genre'], value_vars=['Generic', 'Main'], var_name='CharacterType', value_name='Ratio')
fig3 = px.line(df_tvshows, y="Ratio", x="CharacterType", color="Genre", markers=True)
fig3.update_traces(marker=dict(size=15), line=dict(color='rgb(204, 80, 62)'))
genres = list(df_tvshows.Genre.unique())
negative_slope_genres = [g for g in genres if list(df_tvshows[(df_tvshows['Genre']==g)&(df_tvshows['CharacterType']=='Main')]['Ratio'])[0]-list(df_tvshows[(df_tvshows['Genre']==g)&(df_tvshows['CharacterType']=='Generic')]['Ratio'])[0] < 0]
fig3.for_each_trace(
	lambda trace: trace.update(line=dict(color='rgb(56, 166, 165)')) if trace.name in negative_slope_genres else (),
)

# Main Characters
labels_font_size=15
for g in genres:
	y0 = list(df_tvshows[(df_tvshows['Genre']==g)&(df_tvshows['CharacterType']=='Main')]['Ratio'])[0]
	if g == 'Anime Series':
		dy = 2
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Korean TV Shows':
		dy= 1.7
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Teen TV Shows':
		dy = 1.2
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Mysteries':
		dy = 0.9
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Kids\' TV':
		dy = 0
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Horror':
		dy = -0.2
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Spanish-Language TV Shows':
		dy = -0.3
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Dramas':
		dy = -0.6
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'International TV Shows':
		dy = -0.95
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Sci-Fi & Fantasy':
		dy = 0.5
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Crime TV Shows':
		dy = -0.7
		fig3.add_annotation(x=1.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	else:
		fig3.add_annotation(x=1.4, y=y0, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='left', width=280)
		fig3.add_shape(type='line', x0=1, x1=1.06, y0=y0, y1=y0, line_color='black', xref='x', yref='y', layer='below', line_width=1)

# Generic Characters
for g in genres:
	y0 = list(df_tvshows[(df_tvshows['Genre']==g)&(df_tvshows['CharacterType']=='Generic')]['Ratio'])[0]
	if g == 'Romantic TV Shows':
		dy = 0.8
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Teen TV Shows':
		dy = 0.8
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Anime Series':
		dy = 2
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Thrillers':
		dy = 1.6
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'Kids\' TV':
		dy = 1.2
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'TV Mysteries':
		dy = 1.3
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'International TV Shows':
		dy = 0.9
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'TV Horror':
		dy = -0.5
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'Spanish-Language TV Shows':
		dy = -0.8
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	elif g == 'Reality TV':
		dy = -0.2
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'TV Comedies':
		dy = -1
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)			
	elif g == 'British TV Shows':
		dy = -0.7
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'Crime TV Shows':
		dy = -1.2
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
	elif g == 'Stand-Up Comedy & Talk Shows':
		dy = -0.3
		fig3.add_annotation(x=-0.4, y=y0+dy, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0+dy, line_color='black', xref='x', yref='y', layer='below', line_width=1)
	else:
		fig3.add_annotation(x=-0.4, y=y0, text=g, showarrow=False, xref='x', yref='y', font=dict(size=labels_font_size, color='black'), align='right', width=280)
		fig3.add_shape(type='line', x0=0, x1=-0.06, y0=y0, y1=y0, line_color='black', xref='x', yref='y', layer='below', line_width=1)		
# Background
for y in np.arange(18, 60, 1):
	if y%5 != 0:
		fig3.add_shape(type='line', x0=0.05, x1=0.95, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
	else:
		fig3.add_shape(type='line', x0=0.05, x1=0.37, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
		fig3.add_shape(type='line', x0=0.63, x1=0.95, y0=y, y1=y, opacity=0.3, line_color='rgb(102, 102, 102)')
for y in np.arange(20, 60, 5):
	fig3.add_annotation(x=0.5, y=y, text=str(y)+'%', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig3.add_annotation(x=-0.4, y=16, text='<b>Generic<br>Characters</b>', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig3.add_annotation(x=1.4, y=16, text='<b>Main<br>Characters</b>', opacity=0.3, showarrow=False, font=dict(size=30, color='rgb(102, 102, 102)'))
fig3.update_layout(plot_bgcolor='white'
				   ,xaxis_title=None
				   ,yaxis_title=None
				   ,yaxis_visible=False
				   ,xaxis_visible=False
				   ,width=1200
				   ,height=850
				   ,showlegend=False)
fig3.write_html('results/slope_chart_tvshows_genres_general_vs_main.html')
# Add plot on Plotly profile for embedding on Medium
py.plot(fig3, filename='slope_tvshows_genres_division', auto_open = False)