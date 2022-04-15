import clean_data
import create_db
import analyze_data
import pandas as pd

def main():
    data_path = 'data/'
    netflix_df, names_df, names_df_bigger, in_male_names_df, in_female_names_df, extra_names_df, countries_df = create_db.ReadCsv(data_path)
    netflix_df, names_df, names_df_bigger = create_db.RenameColumns(netflix_df, names_df, names_df_bigger)
    in_names_df = pd.concat([in_male_names_df, in_female_names_df], ignore_index=True)
    names_df = pd.concat([in_names_df, names_df], ignore_index=True)
    print(names_df.shape)
    names_df_bigger = names_df_bigger[names_df_bigger['CountryCode']=='US']
    names_df = pd.concat([names_df, names_df_bigger], ignore_index=True)
    print(names_df.shape)
    names_df = pd.concat([names_df, extra_names_df], ignore_index=True)
    print(names_df.shape)
    names_df['Name'] = clean_data.SetTitleSeriesName(names_df['Name'])
    names_df = names_df.drop_duplicates()
    netflix_df = create_db.AddCountryColumninMoviesDataframe(netflix_df, countries_df)
    netflix_df = clean_data.GetSubsetWithCastNotNull(netflix_df) # We select just the movies/tv-shows with a Cast column with valid values
    create_db.CreateDbTables('12345678', 'women_in_netflix', netflix_df, 'Netflix', 'replace')
    clean_data.LabelGenericMoviesGenre() # Update netflix table - clean the movies with Listedin='Movies'
    df = analyze_data.AddGenderCountColumns(netflix_df, names_df)
    analyze_data.SaveCountNotAvailableNamesDict('results/not_available_names.txt', 'results/not_available_names_count.txt')
    df.head()
    create_db.CreateDbTables('12345678', 'women_in_netflix', df, 'GendersCount', 'replace')


if __name__ == '__main__':
    main()