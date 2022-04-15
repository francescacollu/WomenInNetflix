import pandas as pd
import numpy as np
from .. import analyze_data
from .. import clean_data
from sqlalchemy import create_engine

def test_gender_count_standard():
    gender_list = ['F', 'M', 'F', 'F']
    male_count, female_count, unspecified_count, name_not_available = analyze_data.GetGenderCount(gender_list)
    assert male_count == 1
    assert female_count == 3
    assert unspecified_count == 0
    assert name_not_available == 0

def test_gender_count_null():
    gender_list = [0]
    male_count, female_count, unspecified_count, name_not_available = analyze_data.GetGenderCount(gender_list)
    assert male_count == 0
    assert female_count == 0
    assert unspecified_count == 0
    assert name_not_available == 0

def test_getting_cast_names():
    movies_df = pd.read_csv('data/netflix_titles.csv', dtype={'show_id':str, 'type':str, 'title':str, 'director':str, 'cast':str, 'country':str, 'date_added':str, 'release_year':int, 'rating':str, 'duration':str, 'listed_in':str, 'description':str})
    movies_df = movies_df.rename(columns={'show_id':'ShowId', 'type':'Type', 'title':'Title', 'director':'Director', 'cast':'Cast', 'country':'Country', 'date_added':'DateAdded', 'release_year':'ReleaseYear', 'rating':'Rating', 'duration':'Duration', 'listed_in':'ListedIn', 'description':'Description'})
    names_list = analyze_data.GetCastNames(movies_df, 's516')
    assert names_list[0] == 'Saoirse'
    assert names_list[3] == 'Jamie'

def test_getting_gender_list():
    name_list = ['Mel', 'Sue', 'Mary', 'Paul']
    country_code = 'GB'
    names_df = pd.read_csv('data/wgnd_source.csv', dtype={'name':str,'code':str,'gender':str,'src_Albertagvt':str,'src_FB':str,'src_INE':str,'src_INSEE':str,'src_MichaelJ':str,'src_Statistics_Denmark':str,'src_UK_National_St':str,'src_US_Census':str,'src_US_SSA':str,'src_WIPO':str,'src_WIPO_manual':str,'src_Wikipedia':str,'src_Yu_et_al':str,'src_statsweden':str,'gchar12':str,'gchar1':str,'gchar2':str,})
    names_df = names_df.rename(columns={'name':'Name', 'gender':'Gender', 'code':'CountryCode'})
    names_df['Name'] = clean_data.SetTitleSeriesName(names_df['Name'])
    gender_list = analyze_data.GetGenderList(name_list, names_df, country_code)
    assert gender_list[1] == 'F'

def test_if_there_is_no_name_for_that_country():
    names_and_genders_df = pd.DataFrame({'Name':['Zach', 'Zach', 'Kate', 'Hamish'], 'CountryCode':['US', 'ZA', 'ZA', 'IT'], 'Gender':['M', 'F', 'M', '?']})
    cast_names_list = ['Zach', 'Kate', 'Hamish']
    country_code_input = 'ZA'
    gender_list = analyze_data.GetGenderList(cast_names_list, names_and_genders_df, country_code_input)
    assert gender_list[0] == 'M'

def test_count_columns_in_movies_df():
    engine = create_engine('mysql+mysqlconnector://root:'+'12345678'+'@127.0.0.1:3306/'+'women_in_netflix')
    netflix_df = pd.read_sql('SELECT * FROM Netflix;', engine)
    names_df = pd.read_csv('data/wgnd_source.csv', dtype={'name':str,'code':str,'gender':str,'src_Albertagvt':str,'src_FB':str,'src_INE':str,'src_INSEE':str,'src_MichaelJ':str,'src_Statistics_Denmark':str,'src_UK_National_St':str,'src_US_Census':str,'src_US_SSA':str,'src_WIPO':str,'src_WIPO_manual':str,'src_Wikipedia':str,'src_Yu_et_al':str,'src_statsweden':str,'gchar12':str,'gchar1':str,'gchar2':str,})
    names_df = names_df.rename(columns={'name':'Name', 'gender':'Gender', 'code':'CountryCode'})
    names_df['Name'] = clean_data.SetTitleSeriesName(names_df['Name'])
    netflix_df = netflix_df[netflix_df['ShowId']=='s6']
    netflix_df = analyze_data.AddGenderCountColumns(netflix_df, names_df)
    assert list(netflix_df.loc[netflix_df['ShowId']=='s6', 'FemaleCount'])[0] == 5