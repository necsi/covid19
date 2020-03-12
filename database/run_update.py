import json
from covid19_data_aggregator.utils import *
from covid19_data_aggregator.john_hopkins import *
from covid19_data_aggregator.italy import *


# All download URLs for the "Detailed data" Google Sheet
with open('google_sheet_urls.json', encoding='utf-8') as file:
    download_urls = json.loads(file.read())

# Download data from Google Sheets
download_google_sheets('data/google-sheets/', download_urls)

# Download John Hopkins data
download_john_hopkins_data('data/')

download_john_hopkins_confirmed_cases_deltas_time_series('data/')
download_john_hopkins_death_cases_deltas_time_series('data/')
download_john_hopkins_recovered_cases_deltas_time_series('data/')

# Download Italy data
df = download_italy_data('data/')
create_json_for_mapping_software(df, 'mapping-data/')