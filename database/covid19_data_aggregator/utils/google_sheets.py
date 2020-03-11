import pandas as pd
from .csv_to_dataframe import download_csv_to_dataframe


def download_google_sheets(target_directory, download_urls):
    """
    Download all Google Sheets in the "Detailed data" Google Sheet

    :param target_directory: str
    :param download_urls: dict
    :return: None
    """
    # Download all CSV files and convert to dataframes
    dfs = []
    for key in download_urls.keys():
        dfs.append(download_csv_to_dataframe(download_urls[key]))

    # Save all dataframes to CSVs (TODO: merge into standardized format - it's a wild west out there right now)
    download_url_keys = list(download_urls.keys())
    for index, df in enumerate(dfs):
        file_name = f'{target_directory}Detailed data - {download_url_keys[index]}.csv'
        df.to_csv(file_name, index=False)
    return None