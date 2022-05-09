import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from plotly.graph_objs import *
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

username='fcollu'
api_key='KlCMv4upeJgOV69aFpmr'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# Types: TV-Shows and Movies
engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df_type_diff = pd.read_sql('''
SELECT N.Type, SUM(G.MaleCount) AS Male, SUM(G.FemaleCount) AS Female, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(G.NameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
GROUP BY N.Type;
''', engine)

df_type_diff['Error'] = df_type_diff['UnspecifiedCount']+df_type_diff['NameNotAvailable']

fig = px.histogram(df_type_diff, x='Type', y=['Male', 'Female', 'Error'], barmode='group')
fig.update_layout(plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(visible=False)
fig.write_html('results/type_netflix.html')

# Add plot on Plotly profile for embedding on Medium
py.plot(fig, filename="credentials_file", auto_open = False)


# Percentages

# df_type_diff['Sum'] = df_type_diff.sum(axis=1)
# sm_tvshow = list(df_type_diff.loc[df_type_diff['Type']=='TV Show','Male'])[0]
# sf_tvshow = list(df_type_diff.loc[df_type_diff['Type']=='TV Show','Female'])[0]
# se_tvshow = list(df_type_diff.loc[df_type_diff['Type']=='TV Show','Error'])[0]
# sm_movie = list(df_type_diff.loc[df_type_diff['Type']=='Movie','Male'])[0]
# sf_movie = list(df_type_diff.loc[df_type_diff['Type']=='Movie','Female'])[0]
# se_movie = list(df_type_diff.loc[df_type_diff['Type']=='Movie','Error'])[0]
# s_tvshow = list(df_type_diff.loc[df_type_diff['Type']=='TV Show','Sum'])[0]
# s_movie = list(df_type_diff.loc[df_type_diff['Type']=='Movie','Sum'])[0]
# df_type_diff['MalePercentage'] = [sm_tvshow/s_tvshow, sm_movie/s_movie]
# df_type_diff['FemalePercentage'] = [sf_tvshow/s_tvshow, sf_movie/s_movie]
# df_type_diff['ErrorPercentage'] = [se_tvshow/s_tvshow, se_movie/s_movie]

# fig2 = px.bar(df_type_diff, x='Type', y=['MalePercentage', 'FemalePercentage', 'ErrorPercentage'], barmode='group')
# fig2.update_layout(plot_bgcolor='rgb(255,255,255)')
# fig2.update_yaxes(visible=False)
# fig2.write_html('results/type_netflix_percentage.html')