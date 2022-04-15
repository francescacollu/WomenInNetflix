from .. import clean_data
from .. import create_db
import pandas as pd
import numpy as np

def test_split_string_into_list():
    string_test = 'a, b'
    list_test = clean_data.GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'a'
    assert list_test[1] == 'b'

def test_split_string_into_list_without_space_after_comma():
    string_test = 'a,b'
    list_test = clean_data.GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'a'
    assert list_test[1] == 'b'

def test_split_string_into_list_name_surname():
    string_test = 'n1 c1, n2 c2'
    list_test = clean_data.GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'n1 c1'
    assert list_test[1] == 'n2 c2'

def test_getting_name():
    string_test = 'n1 c1, n2 c2 d2'
    list_test = clean_data.GetList(string_test)
    names_list = clean_data.GetNames(list_test)
    assert names_list[0] == 'n1'
    assert names_list[1] == 'n2'

def test_list_names_from_db():
    movies_df = pd.read_csv('data/netflix_titles.csv', dtype={'show_id':str, 'type':str, 'title':str, 'director':str, 'cast':str, 'country':str, 'date_added':str, 'release_year':int, 'rating':str, 'duration':str, 'listed_in':str, 'description':str})
    movies_df = movies_df.rename(columns={'show_id':'ShowId', 'type':'Type', 'title':'Title', 'director':'Director', 'cast':'Cast', 'country':'Country', 'date_added':'DateAdded', 'release_year':'ReleaseYear', 'rating':'Rating', 'duration':'Duration', 'listed_in':'ListedIn', 'description':'Description'})
    names_string = clean_data.GetList(str(movies_df.loc[movies_df['ShowId']=='s6', 'Cast'].values))
    names_string[0] = names_string[0].strip("['")
    assert names_string[0] == 'Kate Siegel'

def test_setting_title_on_series():
    names_df = pd.read_csv('data/wgnd_source.csv', dtype={'name':str,'code':str,'gender':str,'src_Albertagvt':str,'src_FB':str,'src_INE':str,'src_INSEE':str,'src_MichaelJ':str,'src_Statistics_Denmark':str,'src_UK_National_St':str,'src_US_Census':str,'src_US_SSA':str,'src_WIPO':str,'src_WIPO_manual':str,'src_Wikipedia':str,'src_Yu_et_al':str,'src_statsweden':str,'gchar12':str,'gchar1':str,'gchar2':str,})
    names_df = names_df.rename(columns={'name':'Name', 'gender':'Gender', 'code':'Code'})
    #names_df = create_db.ExtractRows(names_df, 'Code', 'US')
    names_series = names_df['Name']
    names_series = clean_data.SetTitleSeriesName(names_series)
    assert names_series.iloc[0] == 'A Hannan'

def test_getting_subset_with_cast_not_null():
    df = pd.DataFrame({'ShowId':['s1', 's2', 's3'], 'Cast':['Tizia', np.nan, 'Caia']})
    print(df)
    df = clean_data.GetSubsetWithCastNotNull(df)
    assert df.shape[0] == 2