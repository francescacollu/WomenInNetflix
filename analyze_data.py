from cmath import nan
from email.errors import CloseBoundaryNotFoundDefect
from itertools import count
#from women_in_netflix import clean_data
import clean_data
import pandas as pd
import numpy as np
import unicodedata

def StripAccents(text):
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

def GetGenderCount(gender_list):
    male_count = gender_list.count('M')
    female_count = gender_list.count('F')
    unspecified_count = gender_list.count('?')
    name_not_available = gender_list.count('NNA')
    return male_count, female_count, unspecified_count, name_not_available

# cast_or_directors parameter refers to the possibility of get 'Cast' names or 'Director' names
def GetNames(netflix_df, show_id, cast_or_directors):
    names_string = clean_data.GetList(str(netflix_df.loc[netflix_df['ShowId']==show_id, cast_or_directors].values))
    names_list = clean_data.GetNames(names_string)
    names_list = [x.replace("Dr. ", "") for x in names_list]
    names_list = [x.strip("['\"]") for x in names_list]
    names_list = [x.replace("'", " ") for x in names_list]
    names_list = [StripAccents(x) for x in names_list]
    names_list = [x.title() for x in names_list]
    for name in names_list:
        if '-' in name:
            i = names_list.index(name)
            name = name[:name.index('-')]
            names_list[i] = name
    return names_list

def GetGenderList(cast_names_list, names_and_genders_df, country_code_input):
    gender_list = []
    f = open('results/not_available_names.txt', 'a')
    names_list_source = list(names_and_genders_df['Name'])
    if country_code_input is np.nan:
        country_code_input = 'US'
    for name in cast_names_list:
        if name in names_list_source:
            countries_corr_to_name = list(names_and_genders_df.loc[names_and_genders_df['Name']==name, 'CountryCode'])
            if (country_code_input not in countries_corr_to_name) & ('US' not in countries_corr_to_name):
                gender_list.append(list(names_and_genders_df.loc[names_and_genders_df['Name']==name, 'Gender'])[0])
            else:
                gender_list.append(list(names_and_genders_df.loc[((names_and_genders_df['CountryCode']==country_code_input) | (names_and_genders_df['CountryCode']=='US')) & (names_and_genders_df['Name']==name), 'Gender'])[0])
        else:
            gender_list.append('NNA') # Name Not Available
            f.write(str(name)+'\n')
    f.close()
    return gender_list

def SaveCountNotAvailableNamesDict(csv_path_list, count_path):
    nan_list = pd.read_csv(csv_path_list, names=['nan_names'], header=None)
    nan_list = list(nan_list['nan_names'])
    nan_set = set(nan_list)
    d = {}
    for e in nan_set:
        d[e] = nan_list.count(e)
    d = dict(sorted(d.items(), key=lambda x:x[1], reverse=True))
    with open(count_path, 'w') as f: 
        for key, value in d.items(): 
            f.write(str(key)+':'+str(value)+'\n')
    return d

def AddGenderCountColumns(netflix_df, names_df):
    netflix_df['MaleCount'] = 0
    netflix_df['FemaleCount'] = 0
    netflix_df['UnspecifiedCount'] = 0
    netflix_df['NameNotAvailable'] = 0
    netflix_df['MainMale'] = 0
    netflix_df['MainFemale'] = 0
    netflix_df['MainUnspecified'] = 0
    netflix_df['MainNotAvailable'] = 0
    netflix_df['DirectorsMaleCount'] = 0
    netflix_df['DirectorsFemaleCount'] = 0
    netflix_df['DirectorsUnspecifiedCount'] = 0
    netflix_df['DirectorsNameNotAvailable'] = 0
    show_id_list = list(netflix_df['ShowId'].unique())
    for (i,id) in enumerate(show_id_list):
        print(str(i+1)+'/'+str(len(show_id_list)))
        names_list = GetNames(netflix_df, id, 'Cast')
        dir_names_list = GetNames(netflix_df, id, 'Director')
        country_movie = list(netflix_df.loc[netflix_df['ShowId']==id, 'CountryCode'])[0]
        gender_list = GetGenderList(names_list, names_df, country_movie)
        dir_gender_list = GetGenderList(dir_names_list, names_df, country_movie)
        male_count, female_count, unspecified_count, name_not_available = GetGenderCount(gender_list)
        main_male, main_female, main_unspecified, main_not_available = GetGenderCount(gender_list[:2])
        dir_male_count, dir_female_count, dir_unspecified_count, dir_name_not_available = GetGenderCount(dir_gender_list)
        netflix_df.loc[netflix_df['ShowId']==id, 'MaleCount'] = male_count
        netflix_df.loc[netflix_df['ShowId']==id, 'FemaleCount'] = female_count
        netflix_df.loc[netflix_df['ShowId']==id, 'UnspecifiedCount'] = unspecified_count
        netflix_df.loc[netflix_df['ShowId']==id, 'NameNotAvailable'] = name_not_available
        netflix_df.loc[netflix_df['ShowId']==id, 'MainMale'] = main_male
        netflix_df.loc[netflix_df['ShowId']==id, 'MainFemale'] = main_female
        netflix_df.loc[netflix_df['ShowId']==id, 'MainUnspecified'] = main_unspecified
        netflix_df.loc[netflix_df['ShowId']==id, 'MainNotAvailable'] = main_not_available
        netflix_df.loc[netflix_df['ShowId']==id, 'DirectorsMaleCount'] = dir_male_count
        netflix_df.loc[netflix_df['ShowId']==id, 'DirectorsFemaleCount'] = dir_female_count
        netflix_df.loc[netflix_df['ShowId']==id, 'DirectorsUnspecifiedCount'] = dir_unspecified_count
        netflix_df.loc[netflix_df['ShowId']==id, 'DirectorsNameNotAvailable'] = dir_name_not_available
    netflix_df = netflix_df[['ShowId', 'MaleCount', 'FemaleCount', 'UnspecifiedCount', 'NameNotAvailable', 'MainMale', 'MainFemale', 'MainUnspecified', 'MainNotAvailable', 'DirectorsMaleCount', 'DirectorsFemaleCount', 'DirectorsUnspecifiedCount', 'DirectorsNameNotAvailable']]
    return netflix_df