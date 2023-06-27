import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score


def game_data():
    path_to_data = "table_data0.csv"
    with open(path_to_data) as data:
        data_of_games = pd.read_csv(data)
    return data_of_games


def model():
    model_of_set = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)
    train = game_data()
    predictors = [
        "team1_games_played",
        "team1_wins",
        "team1_player_quality",
        "team1_injured_players",
        "team2_games_played",
        "team2_wins",
        "team2_player_quality",
        "team2_injured_players"
    ]
    model_of_set.fit(train[predictors], train["outcome"])
    print(model_of_set)
    preds = model_of_set.predict(train[predictors])
    print(preds)
    preds = pd.Series(preds, index=train.index)
    print(preds)
    print(precision_score(train["outcome"], preds))


if __name__ == '__main__':
    print(game_data())
