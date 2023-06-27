import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import lxml.etree as etree


def clean_team_data_saver(what_to_write, file_path):
    """Saves clean data of the teams"""
    # file_path = Path('football_data.csv')
    with open(file_path, 'w', newline='') as file:
        what_to_write.to_csv(file, index=0)


def make_first_team_data(what_to_write):
    """Creates the file with dirty data"""
    file_path = Path('data.csv')
    with open(file_path, 'w', newline="") as file:
        what_to_write.to_csv(file, index=False, header=False)


def read_dataframe(path):
    """Reads the data frame"""
    return pd.read_csv(path, index_col=0)


def clear_the_data(path):
    """Data cleaner for pandas use only the dirty path"""
    data = read_dataframe(path)
    data = data.drop(['Form', 'Pts'], axis=1)
    data.index = data.index.astype(int)
    data = data.rename(columns={'Unnamed: 1': 'Team'})
    data['CS'] = data['CS'].str.rstrip('%').astype(float) / 100
    data['FTS'] = data['FTS'].str.rstrip('%').astype(float) / 100
    return data


def retrive_data(url):
    """Gets the data of a championship table from the website to be cleand"""
    # Replace the URL with the website you want to scrape
    # url = 'https://www.soccerstats.com/leagueview.asp?league=cleague_2022'
    # Send a GET request to the URL
    response = requests.get(url)
    # Raises an error if cannot reach a site
    response.raise_for_status()
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_the_table_of_championship(soup):
    statistic_table = soup.find('h2', string="Statistical table")
    table_body = statistic_table.find_next_sibling('table')
    return table_body


def convert_html_to_pandas(url):
    table_body = get_the_table_of_championship(retrive_data(url))
    pandas_table = pd.read_html(str(table_body))
    make_first_team_data(pandas_table[0])


def data_of_teams(links):
    all_links = [link['href'] for link in links if 'href' in link.attrs]
    links_to_team = []
    for link in all_links[::2]:
        links_to_team.append('https://www.soccerstats.com/' + link)
    # print(links_to_team)
    # print(website)
    for x in links_to_team:
        team_data = retrive_data(x)
        all_tables = team_data.find_all('table')
        all_tables = [all_tables[x] for x in [3]]
        all_tables = pd.read_html(str(all_tables))
        all_tables[0] = all_tables[0].drop(0, axis=1)
        all_tables[0] = all_tables[0].drop(4, axis=1)
        for index_of_x, x in enumerate(all_tables[0][2]):
            all_tables[0][2][index_of_x] = x[0:5]
        for index, table in enumerate(all_tables):
            if index == 0:
                with open(f'table_data{index}.csv', 'a', newline='') as team_data_file:
                    try:
                        table.to_csv(team_data_file, index=False, header=False)
                    except UnicodeEncodeError:
                        pass
    print("complete")


if __name__ == '__main__':
    """Clean data frame 
    index, team, gp, wins, draws, loses, goals for, goals against, GD,
    point per game, clean sheet, failed to score"""
    file_path_dirty_data = Path('data.csv')
    file_path_clean_data = Path('football_data.csv')
    url_for_championship = 'https://www.soccerstats.com/leagueview.asp?league=cleague'
    url_for_championships = ['https://www.soccerstats.com/leagueview.asp?league=cleague',
                             'https://www.soccerstats.com/leagueview.asp?league=cleague_2022']
    # df = read_dataframe(file_path_clean_data)
    for ind, champ_url in enumerate(url_for_championships):
        convert_html_to_pandas(url=champ_url)
        clean_team_data_saver(clear_the_data(file_path_dirty_data), file_path=f'football_data{ind}.csv')
    for urls in url_for_championships:
        website = get_the_table_of_championship(retrive_data(urls))
        links = website.find_all('a')
        data_of_teams(links)
