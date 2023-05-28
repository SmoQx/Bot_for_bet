import csv
from pathlib import Path
import pandas as pd
import numpy as np


def csv_reader():
    times_won = 0
    path = Path("./venv/football_data.csv")
    with open(path, "r") as data_file:
        fieldnamesCSV = csv.DictReader(data_file).fieldnames
        readerCSV = csv.DictReader(data_file, fieldnames=fieldnamesCSV)
        for line in readerCSV:
            print(line)
            if line["outcome"] == "1":
                times_won += 1
        print(times_won)
        with open(path) as csv_file:
            csv_to_list = csv.reader(csv_file)
            dictionarry_for_data = list(csv_to_list)
            print(dictionarry_for_data[0][0], "\n", dictionarry_for_data[1][0])
    

def read_data_with_pandas():
    data_with_pandas = pd.read_csv('./venv/football_data.csv')
    print(data_with_pandas.head())
    team1_games_played = data_with_pandas.groupby('team1_games_played')['team1_wins'].mean()
    print(team1_games_played)
    data_taken = data_with_pandas[data_with_pandas['team1_games_played'] == '8'][data_with_pandas['team1_wins'] == '4']
    print(data_taken)


def what_pi():
    the_value_of_pi = np.pi
    print(f"{the_value_of_pi: .3f}")


if __name__ == '__main__':
    read_data_with_pandas()