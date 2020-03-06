import requests
import csv
import pandas as pd
from contextlib import closing
import codecs
import numpy as np


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

# All download URLs for the "Detailed data" Google Sheet


download_urls = {'South Korea': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=428126019',
                 'Lebanon': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=572185248',
                 'Italy': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=1872189130',
                 'Iran': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=363880533',
                 'Isreal': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=2050829299',
                 'Spain': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=1840632470',
                 'England': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=192925797',
                 'Japan': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=658839733',
                 'France': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=1242716699',
                 'Argentina': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=61190433',
                 'Brazil': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=1806215787',
                 'Peru': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=1988460402',
                 'Chile': 'https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/export?format=csv&gid=768474154'}


# Download all CSV files and convert to dataframes
dfs = []
for key in download_urls.keys():
    dfs.append(download_csv_to_dataframe(download_urls[key]))

# Save all dataframes to CSVs (TODO: merge into standardized format - it's a wild west out there right now)
download_url_keys = list(download_urls.keys())
for index, df in enumerate(dfs):
    file_name = f'google-sheets-downloads/Detailed data - {download_url_keys[index]}.csv'
    df.to_csv(file_name, index=False)