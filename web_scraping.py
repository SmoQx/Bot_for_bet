import csv

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import lxml.etree as etree


def clean_team_data_saver(what_to_write):
    """Saves clean data of the teams"""
    file_path = Path('football_data.csv')
    with open(file_path, 'w', newline='') as file:
        what_to_write.to_csv(file)


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
    clean_team_data_saver(data)


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


def convert_html_to_pandas():
    table_body = get_the_table_of_championship(retrive_data(url_for_championship))
    pandas_table = pd.read_html(str(table_body))
    make_first_team_data(pandas_table[0])


if __name__ == '__main__':
    """Clean data frame 
    index, team, gp, wins, draws, loses, goals for, goals against, GD,
    point per game, clean sheet, failed to score"""
    file_path_dirty_data = Path('data.csv')
    file_path_clean_data = Path('football_data.csv')
    url_for_championship = 'https://www.soccerstats.com/leagueview.asp?league=cleague'
    # df = read_dataframe(file_path_clean_data)
    website = get_the_table_of_championship(retrive_data(url_for_championship))
    links = website.find_all('a')
    all_links = [link['href'] for link in links if 'href' in link.attrs]
    links_to_team = []
    for link in all_links[::2]:
        links_to_team.append('https://www.soccerstats.com/' + link)
    print(links_to_team)
    # print(website)
    team_data = retrive_data(links_to_team[0])
    all_tables = team_data.find_all('table')
    all_tables = [all_tables[x] for x in [3, 4, 7]]
    all_tables = pd.read_html(str(all_tables))
    for index, table in enumerate(all_tables):
        with open(f'table_data{index}.csv', 'w') as team_data_file:
            try:
                table.to_csv(team_data_file, index=False, header=False)
            except UnicodeEncodeError:
                pass
    """with open('team_data.csv', 'w', newline='') as team_file:
        for table in all_tables:
            try:
                table.to_csv(team_file, index=False, header=False)
            except UnicodeEncodeError:
                pass"""
            