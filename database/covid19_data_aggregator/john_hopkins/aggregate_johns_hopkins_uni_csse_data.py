import pandas as pd
from datetime import datetime
import numpy as np
from ..utils.github import *
from ..utils.csv_to_dataframe import download_csv_to_dataframe

def download_john_hopkins_data(target_directory):
    """
    Download the Johns Hopkins data

    :param target_directory: str
    :return None
    """

    # Get list of CSV files to download from the Johns Hopkins repo
    github_url = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
    extensions_to_ignore = ['.gitignore', '.md']
    file_names = list_github_files(github_url, extensions_to_ignore)

    # Download all CSV files and convert to dataframes
    dfs = []
    base_csv_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    for file_name in file_names:
        csv_url = base_csv_url + file_name
        dfs.append(download_csv_to_dataframe(csv_url))

    # Merge the dataframes
    df = pd.concat(dfs, ignore_index=True, sort=False)

    # Clean up the dates
    cleaned_last_updated = []
    for date_time in df["Last Updated"].values:
        if ' ' in date_time:
            date_time_split = date_time.split()
            if date_time_split[0].endswith('/20'):
                cleaned_last_updated.append(datetime.strptime(date_time, '%m/%d/%y %H:%M'))
            else:
                cleaned_last_updated.append(datetime.strptime(date_time, '%m/%d/%Y %H:%M'))
        else:
            cleaned_last_updated.append(datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S'))
    df = df.drop(['Last Updated'], axis=1)
    df["Last Updated"] = cleaned_last_updated

    # Merge the Province/State columns
    df.columns = ['Province/State', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Province/State2', 'Latitude', 'Longitude', 'Last Updated']
    df['Province/State'].fillna(df['Province/State2'], inplace=True)
    del df['Province/State2']

    # Add empty City, Region, and Source columns
    df['City'] = np.repeat(np.nan, df.shape[0])
    df['Region'] = np.repeat(np.nan, df.shape[0])
    df['Source'] = np.repeat('https://github.com/CSSEGISandData/COVID-19', df.shape[0])

    # Reorder columns
    df = df[['Country/Region', 'Region', 'Province/State', 'City', 'Latitude', 'Longitude', 'Confirmed', 'Deaths', 'Recovered', 'Last Updated', 'Source']]

    # Save to csv (optional)
    df.to_csv(f'{target_directory}john-hopkins-csse-data.csv', index=False)


def to_int(x):
    """
    Try to convert a string to int

    :param x: str
    :return: int or np.nan
    """

    try:
        return int(x)
    except:
        return np.nan


def create_new_delta_columns(df):
    """
    Calculate deltas between all date columns and store
    result as new dataframe

    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """

    new_column_names = [f'{each} Delta' for each in df.columns[5:]]

    # Calculate deltas for each row
    df_as_np = df[df.columns[4:]].values
    row_deltas_list = []
    for row in df_as_np:
        row_deltas_list.append([to_int(j)-to_int(i) for i, j in zip(row[:-1], row[1:])])
    row_deltas_list = list(zip(*row_deltas_list))

    # Add deltas as new columns
    my_dict = {}
    for i, new_column_name in enumerate(new_column_names):
        my_dict[new_column_name] = list(row_deltas_list[i])
    new_df = pd.DataFrame.from_dict(my_dict)
    cases_time_series_df = pd.concat([df.reset_index(drop=True), new_df], axis=1, sort=False)
    return cases_time_series_df


def download_john_hopkins_confirmed_cases_deltas_time_series(target_directory):
    """
    Download Johns Hopkins confirmed cases time series data
    and calculate deltas

    :param target_directory: str
    :return None
    """

    df = download_csv_to_dataframe('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

    cases_time_series_df = create_new_delta_columns(df)

    # Save dataframe
    cases_time_series_df.to_csv(f'{target_directory}john-hopkins-confirmed-cases-deltas-time-series.csv', index=False)
    return None


def download_john_hopkins_death_cases_deltas_time_series(target_directory):
    """
    Download Johns Hopkins death cases time series data
    and calculate deltas

    :param target_directory: str
    :return None
    """

    df = download_csv_to_dataframe('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')

    cases_time_series_df = create_new_delta_columns(df)

    # Save dataframe
    cases_time_series_df.to_csv(f'{target_directory}john-hopkins-death-cases-deltas-time-series.csv', index=False)
    return None


def download_john_hopkins_recovered_cases_deltas_time_series(target_directory):
    """
    Download Johns Hopkins recovered cases time series data
    and calculate deltas

    :param target_directory: str
    :return None
    """

    df = download_csv_to_dataframe('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

    cases_time_series_df = create_new_delta_columns(df)

    # Save dataframe
    cases_time_series_df.to_csv(f'{target_directory}john-hopkins-recovered-cases-deltas-time-series.csv', index=False)
    return None
