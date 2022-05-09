from fileinput import filename
from matplotlib.pyplot import legend
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import math
import chart_studio.plotly as py
import chart_studio.tools as tls
from credential_file import *

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file

engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
df = pd.read_sql('''
SELECT SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(G.NameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId;
''', engine)
df['Unclassified'] = df['UnspecifiedCount']+df['NameNotAvailable']

df['MaleRatio'] = (df['MaleCount']/(df['MaleCount']+df['FemaleCount']))*1000
df['FemaleRatio'] = (df['FemaleCount']/(df['MaleCount']+df['FemaleCount']))*1000

def GetDecimalPart(n):
    n = str(n)
    n = int(n.split('.')[1])
    return n

# This is a function that I 'stole' from https://chart-studio.plotly.com/~empet/15229/heatmap-with-a-discrete-colorscale/#/
def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)     
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values
    
    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale 

def WaffleChartGenderDistribution(df, title, filename_input):
    rows= 20
    cols= 50

    n_col_male_ratio = round(int(list(df.MaleRatio)[0]/rows))
    n_col_female_ratio = round(int(list(df.FemaleRatio)[0]/rows))
    n_row_female_ratio = round(int(str(GetDecimalPart(list(df.FemaleRatio)[0]))[:2])*rows/1000)

    z = np.ones((rows, cols))
    z[:, :n_col_male_ratio] = 1
    z[:, -n_col_female_ratio:] = 2
    z[:n_row_female_ratio, -n_col_female_ratio-1] = 2

    #dictionary that maps the heatmap z-values to strings
    d = {1: 'Male', 2: 'Female'}
    M = max([len(s) for s in d.values()])
    customdata= np.empty((rows,cols), dtype=f'<U{M}')  #supplementary information on each waffle cell

    for i in range(rows):
        for j in range(cols):           
            customdata[i,j] = d[z[i, j]] 

    bvals = [0, 1, 2]
    colors = ['#1F77B4', '#FF7F0E']
    dcolorsc = discrete_colorscale(bvals, colors)

    bvals = np.array(bvals)
    tickvals = [1.25, 1.75] 
    ticktext = ['Male ('+str(round(list(df.MaleRatio)[0]/10, 2))+'%)', 'Female ('+str(round(list(df.FemaleRatio)[0]/10, 2))+'%)']
    heatmap = go.Heatmap(z=z, 
                        customdata=customdata, xgap=1, ygap=1,
                        colorscale = dcolorsc, 
                        colorbar = dict(thickness=20, 
                                        len=0.2,
                                        tickvals=tickvals, 
                                        ticktext=ticktext))
    fig = go.Figure(data=[heatmap])
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update(data=[{'customdata': customdata,
        'hovertemplate': '%{customdata}<extra></extra>',
        'xgap':1, 'ygap':1}])
    fig.update_layout(title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.write_html('results/'+filename_input+'.html')

    # Add plot on Plotly profile for embedding on Medium
    py.plot(fig, filename=filename_input, auto_open = False)

WaffleChartGenderDistribution(df, 'Gender Distribution on US Netflix Catalogue', 'whole_netflix_gender_distribution')

# Let's distinguish between movies and tv-shows
df = pd.read_sql('''
SELECT SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(G.NameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type='Movie';
''', engine)
df['Unclassified'] = df['UnspecifiedCount']+df['NameNotAvailable']

df['MaleRatio'] = (df['MaleCount']/(df['MaleCount']+df['FemaleCount']))*1000
df['FemaleRatio'] = (df['FemaleCount']/(df['MaleCount']+df['FemaleCount']))*1000

WaffleChartGenderDistribution(df, 'Gender Distribution on US Netflix Movies', 'waffle_chart_movies')


df = pd.read_sql('''
SELECT SUM(G.MaleCount) AS MaleCount, SUM(G.FemaleCount) AS FemaleCount, SUM(G.UnspecifiedCount) AS UnspecifiedCount, SUM(G.NameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type='TV Show';
''', engine)
df['Unclassified'] = df['UnspecifiedCount']+df['NameNotAvailable']

df['MaleRatio'] = (df['MaleCount']/(df['MaleCount']+df['FemaleCount']))*1000
df['FemaleRatio'] = (df['FemaleCount']/(df['MaleCount']+df['FemaleCount']))*1000

WaffleChartGenderDistribution(df, 'Gender Distribution on US Netflix TV-Shows', 'waffle_chart_tvshows')


# What about directors?
df = pd.read_sql('''
SELECT SUM(G.DirectorsMaleCount) AS MaleCount, SUM(G.DirectorsFemaleCount) AS FemaleCount, SUM(G.DirectorsUnspecifiedCount) AS UnspecifiedCount, SUM(G.DirectorsNameNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId
WHERE N.Type='Movie';
''', engine)
df['Unclassified'] = df['UnspecifiedCount']+df['NameNotAvailable']
df['MaleRatio'] = (df['MaleCount']/(df['MaleCount']+df['FemaleCount']))*1000
df['FemaleRatio'] = (df['FemaleCount']/(df['MaleCount']+df['FemaleCount']))*1000

WaffleChartGenderDistribution(df, 'Directors Gender Distribution on US Netflix Catalogue', 'waffle_chart_directors')


# Main characters
df = pd.read_sql('''
SELECT SUM(G.MainMale) AS MaleCount, SUM(G.MainFemale) AS FemaleCount, SUM(G.MainUnspecified) AS UnspecifiedCount, SUM(G.MainNotAvailable) AS NameNotAvailable
FROM GendersCount G LEFT JOIN Netflix N ON G.ShowId=N.ShowId;
''', engine)
df['Unclassified'] = df['UnspecifiedCount']+df['NameNotAvailable']
df['MaleRatio'] = (df['MaleCount']/(df['MaleCount']+df['FemaleCount']))*1000
df['FemaleRatio'] = (df['FemaleCount']/(df['MaleCount']+df['FemaleCount']))*1000

WaffleChartGenderDistribution(df, 'Main Characters Gender Distribution on US Netflix Catalogue', 'waffle_chart_main_characters')
