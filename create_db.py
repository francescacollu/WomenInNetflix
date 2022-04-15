import pandas as pd
from sqlalchemy import create_engine

def ReadCsv(path):
    movies_df = pd.read_csv(path+'netflix_titles.csv', dtype={'show_id':str, 'type':str, 'title':str, 'director':str, 'cast':str, 'country':str, 'date_added':str, 'release_year':int, 'rating':str, 'duration':str, 'listed_in':str, 'description':str})
    names_df = pd.read_csv(path+'wgnd_source.csv', dtype={'name':str,'code':str,'gender':str}, usecols=['name', 'gender', 'code'])[['name', 'gender', 'code']]
    names_df_bigger = pd.read_csv(path+'wgnd_langctry.csv', dtype={'name':str,'gender':str,'code':str}, usecols=['name', 'gender', 'code'])[['name', 'gender', 'code']]
    in_male_names_df = pd.read_csv(path+'Indian-Male-Names.csv', dtype={'Name':str, 'Gender':str, 'CountryCode':str})
    in_female_names_df = pd.read_csv(path+'Indian-Female-Names.csv', dtype={'Name':str, 'Gender':str, 'CountryCode':str})
    extra_names_df = pd.read_csv(path+'ExtraNames.csv', dtype={'Name':str, 'Gender':str, 'CountryCode':str})
    countries_df = pd.read_csv(path+'country_list.csv', dtype={'Name':str, 'Code':str})
    return movies_df, names_df, names_df_bigger, in_male_names_df, in_female_names_df, extra_names_df, countries_df

def ExtractColumns(df, columns_list):
    df = df[columns_list]
    return df

def ExtractRows(df, column_for_condition, value_condition):
    df = df[df[column_for_condition] == value_condition]
    return df

def RenameColumns(movies_df, names_df, names_df_bigger):
    movies_df = movies_df.rename(columns={'show_id':'ShowId', 'type':'Type', 'title':'Title', 'director':'Director', 'cast':'Cast', 'country':'Country', 'date_added':'DateAdded', 'release_year':'ReleaseYear', 'rating':'Rating', 'duration':'Duration', 'listed_in':'ListedIn', 'description':'Description'})
    names_df = names_df.rename(columns={'name':'Name', 'gender':'Gender', 'code':'CountryCode'})
    names_df_bigger = names_df_bigger.rename(columns={'name':'Name', 'gender':'Gender', 'code':'CountryCode'})
    return movies_df, names_df, names_df_bigger

def AddCountryColumninMoviesDataframe(movies_df, countries_df):
    movies_df = movies_df.merge(countries_df, how='left', left_on='Country', right_on='Name')
    movies_df = movies_df.loc[:, movies_df.columns!='Name']
    movies_df = movies_df.rename(columns={'Code':'CountryCode'})
    return movies_df

def CreateDbTables(password, db_name, df, table_name, if_exist):
    engine = create_engine('mysql+mysqlconnector://root:'+password+'@127.0.0.1:3306/'+db_name)
    df.to_sql(name=table_name, con=engine, if_exists=if_exist, index=False)

def AddPrimaryKey(password, db_name, table_name, pk_column_name):
    engine = create_engine('mysql+mysqlconnector://root:'+password+'@127.0.0.1:3306/'+db_name)
    with engine.connect() as conn:
        conn.execute('ALTER TABLE '+table_name+' ADD PRIMARY KEY ('+pk_column_name+');')