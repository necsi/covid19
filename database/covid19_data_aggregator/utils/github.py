import requests
from bs4 import BeautifulSoup


def list_github_files(url, ext_to_ignore=[]):
    """
    Get a list of files in a folder inside a GitHub repository.

    :param url: str
    :param ext_to_ignore: list
    :return: list
    """
    response = requests.get(url)
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
        filtered_file_names = [file_name for file_name in file_names if not file_name.endswith(tuple(ext_to_ignore))]
    return filtered_file_names