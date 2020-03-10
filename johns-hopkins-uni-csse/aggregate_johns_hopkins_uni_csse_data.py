import requests
from contextlib import closing
import csv
import numpy as np
import codecs
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def list_github_files(url, ext_to_ignore=[]):
    """
    Get a list of files in a folder inside a GitHub repository.

    :param url: str
    :param ext_to_ignore: list
    :return: list
    """
    response = requests.get(list_of_csvs)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table', {'class': 'files js-navigation-container js-active-navigation-container'})[0]
    rows = table.find_all('tr')
    file_names = []
    for row in rows:
        content_column = row.find_all('td', {'class': 'content'})
        if content_column:
            content_column_link_tag = content_column[0].find('a')
            if content_column_link_tag:
                file_names.append(content_column_link_tag.text)
    if ext_to_ignore:
        filtered_file_names = [file_name for file_name in file_names if not file_name.endswith(tuple(extensions_to_ignore))]
    return filtered_file_names


def download_csv_to_dataframe(url):
    """
    Download a CSV file and return a Pandas DataFrame.

    :param url: str
    :return: pandas.DataFrame
    """
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
        data = [row for row in reader]
        header_row = data[0]
        data = data[1:]
        df = pd.DataFrame(data = data, index=np.arange(1, len(data)+1), columns=header_row)
        return df


# Get list of CSV files to download from the Johns Hopkins repo
list_of_csvs = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
extensions_to_ignore = ['.gitignore', '.md']
file_names = list_github_files(list_of_csvs, extensions_to_ignore)

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
for date_time in df["Last Update"].values:
    if ' ' in date_time:
        date_time_split = date_time.split()
        if date_time_split[0].endswith('/20'):
            cleaned_last_updated.append(datetime.strptime(date_time, '%m/%d/%y %H:%M'))
        else:
            cleaned_last_updated.append(datetime.strptime(date_time, '%m/%d/%Y %H:%M'))
    else:
        cleaned_last_updated.append(datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S'))
df = df.drop(['Last Update'], axis=1)
df["Last Update"] = cleaned_last_updated

# Merge the Province/State columns
df.columns = ['Province/State', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Province/State2', 'Latitude', 'Longitude', 'Last Update']
df['Province/State'].fillna(df['Province/State2'], inplace=True)
del df['Province/State2']

# Add empty City, Region, and Source columns
df['City'] = np.repeat(np.nan, df.shape[0])
df['Region'] = np.repeat(np.nan, df.shape[0])
df['Source'] = np.repeat('https://github.com/CSSEGISandData/COVID-19', df.shape[0])

# Reorder columns
df = df[['Country/Region', 'Region', 'Province/State', 'City', 'Latitude', 'Longitude', 'Confirmed', 'Deaths', 'Recovered', 'Last Update', 'Source']]

# Save to csv (optional)
df.to_csv('johns-hopkins-uni-csse/jhu-csse-data.csv', index=False)
