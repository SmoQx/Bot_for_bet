import pandas as pd
import subprocess
from pathlib import Path


def does_exist():
    files_for_data = ["./table_data0.csv", "./football_data0.csv", "./football_data1.csv"]
    for file in files_for_data:
        file = Path(file)
        if not Path.exists(file):
            subprocess.run(['python', 'web_scraping.py'])
        else:
            print(f"Ok! {file}")


def check_values():
    if len(game_played()) != 501:
        game_played('w')
    else:
        print('not empty')


def game_played(read_write='r'):
    path_to_data = "table_data0.csv"
    if read_write != 'r':
        with open(path_to_data, 'w') as data:
            pass
        print(f"Usunięto dane z {path_to_data} generuje nowe")
        subprocess.run(['python', 'web_scraping.py'])
    else:
        with open(path_to_data, read_write) as data:
            columns = ['team1', 'score', 'team2']
            data_of_games = pd.read_csv(data, names=columns)
        return data_of_games


def championship_scores(path):
    with open(path) as data:
        data_of_games = pd.read_csv(data)
    return data_of_games


if __name__ == '__main__':
    does_exist()

    path_to_championship_data = ["football_data0.csv", "football_data1.csv"]

    """if len(game_played()) != 500:
        game_played('w')
    else:
        print('not empty')"""
