import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
from ..utils.csv_to_dataframe import download_csv_to_dataframe


def clean_italy_data(df):
    """
    Clean italy data

    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df = df[['data', 'stato', 'denominazione_regione', 'denominazione_provincia', 'lat', 'long', 'totale_casi']]
    df.columns = ['Last Updated', 'Country/Region', 'Region', 'Province/State', 'Latitude', 'Longitude', 'Confirmed']
    df['Confirmed'] = df.Confirmed.apply(lambda x: int(x))

    # Add expected columns
    df_rows = df.shape[0]
    df['City'] = np.repeat(np.nan, df_rows)
    df['Deaths'] = np.repeat(np.nan, df_rows)
    df['Recovered'] = np.repeat(np.nan, df_rows)
    df['Source'] = np.repeat('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv', df_rows)

    # Reorder columns
    df = df[['Country/Region', 'Region', 'Province/State', 'City', 'Latitude', 'Longitude', 'Confirmed', 'Deaths', 'Recovered', 'Last Updated', 'Source']]

    df['Country/Region'] = df['Country/Region'].apply(lambda x: 'Italy')
    return df


def create_json_for_mapping_software(df, target_directory):
    """
    Clean italy data

    :param target_directory: str 
    :param df: pandas.DataFrame
    :return: None
    """
    # Convert Last Updated to datetime object
    df['Last Updated'] = df['Last Updated'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    
    # Group by province
    confirmed_by_region = df.groupby(['Region']).sum()[['Confirmed']].apply(lambda g: g.values.tolist()).to_dict()['Confirmed']

    # Get daily confirmed case deltas
    yesterday = datetime.now() - timedelta(days=1)
    day_before_yesterday = datetime.now() - timedelta(days=2)
    yesterday_confirmed_count_by_region = df[df['Last Updated'] >= yesterday].sort_values(by=['Last Updated']).groupby(['Region']).sum()[['Confirmed']].apply(lambda g: g.values.tolist()).to_dict()['Confirmed']
    day_before_yesterday_confirmed_count_by_region = df[(df['Last Updated'] >= day_before_yesterday) & (df['Last Updated'] <= yesterday)].sort_values(by=['Last Updated']).groupby(['Region']).sum()[['Confirmed']].apply(lambda g: g.values.tolist()).to_dict()['Confirmed']
    
    # Create required dictionary structure
    format_for_map = {}
    for key, value in yesterday_confirmed_count_by_region.items():
        delta = value - day_before_yesterday_confirmed_count_by_region[key]
        format_for_map[key] = {'scalerank': confirmed_by_region[key], 'one_day': delta}

    # Save dictionary as json file
    with open(f'{target_directory}italy-confirmed-by-region.json', 'w') as json_file:
        json.dump(format_for_map, json_file)
    return None


def download_italy_data(target_directory):
    """
    Downloads a CSV and returns a pandas DataFrame

    :param target_directory: str
    :return: pandas.DataFrame
    """
    # Download CSV to pandas Dataframe
    df = download_csv_to_dataframe('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv')

    # Clean data
    df = clean_italy_data(df)

    # Save CSV for later aggregation
    df.to_csv(f'{target_directory}italy-data.csv', index=False)
    return df
