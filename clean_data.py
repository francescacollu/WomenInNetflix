import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def GetList(input_string):
    output_list = input_string.split(',')
    for i in range(len(output_list)):
        output_list[i] = output_list[i].strip()
    return output_list

def GetNames(input_list):
    name_list = [x.split()[0] for x in input_list]
    return name_list

def SetTitleSeriesName(series_input):
    return series_input.str.title()

def GetSubsetWithCastNotNull(df):
    df = df[df['Cast'].notnull()]
    return df

def LabelGenericMoviesGenre():
    engine = create_engine('mysql+mysqlconnector://root:12345678@127.0.0.1:3306/women_in_netflix')
    with engine.connect() as conn:
        conn.execute('''UPDATE Netflix
                        SET ListedIn = (
                            CASE WHEN ShowId='s309' THEN 'Documentaries'
                                 WHEN ShowId='s471' THEN 'Reality TV'
                                 WHEN ShowId='s730' THEN 'Reality TV'
                                 WHEN ShowId='s731' THEN 'Reality TV'
                                 WHEN ShowId='s733' THEN 'Reality TV'
                                 WHEN ShowId='s2910' THEN 'Children & Family Movies'
                                 WHEN ShowId='s2961' THEN 'Action & Adventures'
                                 WHEN ShowId='s2965' THEN 'Documentaries'
                                 WHEN ShowId='s3315' THEN 'Children & Family Movies'
                                 WHEN ShowId='s3347' THEN 'Dramas, Comedies'
                                 WHEN ShowId='s4139' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4279' THEN 'Anime Features'
                                 WHEN ShowId='s4345' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4491' THEN 'Comedies'
                                 WHEN ShowId='s4492' THEN 'Reality TV'
                                 WHEN ShowId='s4498' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4746' THEN 'Comedies'
                                 WHEN ShowId='s4893' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4894' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4895' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4896' THEN 'Children & Family Movies'
                                 WHEN ShowId='s4897' THEN 'Children & Family Movies'
                                 WHEN ShowId='s5017' THEN 'TV Comedies'
                                 WHEN ShowId='s5018' THEN 'TV Comedies'
                                 WHEN ShowId='s5020' THEN 'TV Comedies'
                                 WHEN ShowId='s5024' THEN 'Reality TV'
                                 WHEN ShowId='s5542' THEN 'Stand-Up Comedy, Comedies'
                                 WHEN ShowId='s5660' THEN 'Children & Family Movies'
                                 WHEN ShowId='s5735' THEN 'Children & Family Movies'
                                 WHEN ShowId='s5776' THEN 'Children & Family Movies'
                                 WHEN ShowId='s5795' THEN 'Stand-Up Comedy, Comedies'
                                 WHEN ShowId='s5814' THEN 'Stand-Up Comedy, Comedies'
                                 WHEN ShowId='s5877' THEN 'Action & Adventures'
                                 WHEN ShowId='s5921' THEN 'Comedies'
                                 WHEN ShowId='s5990' THEN 'Documentaries'
                                 WHEN ShowId='s6462' THEN 'Children & Family Movies'
                                 WHEN ShowId='s6464' THEN 'Children & Family Movies'
                                 WHEN ShowId='s6812' THEN 'Documentaries'
                                 WHEN ShowId='s6813' THEN 'Documentaries'
                                 WHEN ShowId='s7117' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7277' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7278' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7406' THEN 'Documentaries'
                                 WHEN ShowId='s7619' THEN 'Documentaries'
                                 WHEN ShowId='s7723' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7775' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7777' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7779' THEN 'Children & Family Movies'
                                 WHEN ShowId='s7782' THEN 'Children & Family Movies'
                                 WHEN ShowId='s8006' THEN 'Children & Family Movies'
                                 WHEN ShowId='s8007' THEN 'Children & Family Movies'
                                 WHEN ShowId='s8008' THEN 'Children & Family Movies'
                                 WHEN ShowId='s8760' THEN 'Reality TV'
                            END
                        ),
                        Type = (
                            CASE WHEN ShowId='s471' THEN 'TV Show'
                                 WHEN ShowId='s730' THEN 'TV Show'
                                 WHEN ShowId='s731' THEN 'TV Show'
                                 WHEN ShowId='s733' THEN 'TV Show'
                                 WHEN ShowId='s4492' THEN 'TV Show'
                                 WHEN ShowId='s5017' THEN 'TV Show'
                                 WHEN ShowId='s5018' THEN 'TV Show'
                                 WHEN ShowId='s5020' THEN 'TV Show'
                                 WHEN ShowId='s5024' THEN 'TV Show'
                                 WHEN ShowId='s8760' THEN 'TV Show'
                            END
                        )
                        WHERE ShowId IN 
                        ('s309',
                         's471',
                         's730',
                         's731',
                         's733',
                         's2910',
                         's2961',
                         's2965',
                         's3315',
                         's3347',
                         's4139',
                         's4279',
                         's4345',
                         's4491',
                         's4492',
                         's4498',
                         's4746',
                         's4893',
                         's4894',
                         's4895',
                         's4896',
                         's4897',
                         's5017',
                         's5018',
                         's5020',
                         's5024',
                         's5542',
                         's5660',
                         's5735',
                         's5776',
                         's5795',
                         's5814',
                         's5877',
                         's5921',
                         's5990',
                         's6462',
                         's6464',
                         's6812',
                         's6813',
                         's7117',
                         's7277',
                         's7278',
                         's7406',
                         's7619',
                         's7723',
                         's7775',
                         's7777',
                         's7779',
                         's7782',
                         's8006',
                         's8007',
                         's8008',
                         's8760')
                        ;''')