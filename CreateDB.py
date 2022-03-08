import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

movies_df = pd.read_csv('data/netflix_titles.csv')
names_df = pd.read_csv('data/wgnd_langctry.csv')
country_df = pd.read_csv('data/country_list.csv')