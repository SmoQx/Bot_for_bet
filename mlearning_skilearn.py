from data_reader import game_played, championship_scores
import numpy as np


def open_game_data():
    data_frame = game_played()
    return data_frame


def open_championship_data(path):
    data_frame = championship_scores(path)
    return data_frame


def calculate_likelihood(team1, team2):
    path_to_championship_data = ["football_data0.csv", "football_data1.csv"]
    team_stats_df = open_championship_data(path_to_championship_data[0])
    game_scores_df = open_game_data()
    # Step 1: Input team names
    team1 = team1.strip()
    team2 = team2.strip()

    # Step 2: Find corresponding rows for the teams
    team1_stats = team_stats_df.loc[team_stats_df['Team'] == team1]
    team2_stats = team_stats_df.loc[team_stats_df['Team'] == team2]

    # Step 3: Calculate likelihood scores
    try:
        team1_goals_scored = game_scores_df[(game_scores_df['team1'] == team1) &
                                            (game_scores_df['team2'] == team2)]['score'].apply(lambda x: int(x.split('-')[0].strip()))
        team1_goals_conceded = game_scores_df[(game_scores_df['team1'] == team2) &
                                              (game_scores_df['team2'] == team1)]['score'].apply(lambda x: int(x.split('-')[1].strip()))

        team2_goals_scored = game_scores_df[(game_scores_df['team1'] == team2) &
                                            (game_scores_df['team2'] == team1)]['score'].apply(lambda x: int(x.split('-')[0].strip()))
        team2_goals_conceded = game_scores_df[(game_scores_df['team1'] == team1) &
                                              (game_scores_df['team2'] == team2)]['score'].apply(lambda x: int(x.split('-')[1].strip()))

        team1_likelihood = (
            team1_stats['W'].values[0] * team1_stats['GF'].values[0] * team2_stats['L'].values[0] *
            team2_stats['GA'].values[0] * team1_goals_scored.mean() * team2_goals_conceded.mean() /
            (team1_stats['W'].values[0] * team1_stats['GF'].values[0] * team2_stats['L'].values[0] *
             team2_stats['GA'].values[0] * team1_goals_scored.mean() * team2_goals_conceded.mean() +
             team2_stats['W'].values[0] * team2_stats['GF'].values[0] * team1_stats['L'].values[0] *
             team1_stats['GA'].values[0] * team2_goals_scored.mean() * team1_goals_conceded.mean())
        )
        team2_likelihood = (
            team2_stats['W'].values[0] * team2_stats['GF'].values[0] * team1_stats['L'].values[0] *
            team1_stats['GA'].values[0] * team2_goals_scored.mean() * team1_goals_conceded.mean() /
            (team2_stats['W'].values[0] * team2_stats['GF'].values[0] * team1_stats['L'].values[0] *
             team1_stats['GA'].values[0] * team2_goals_scored.mean() * team1_goals_conceded.mean() +
             team1_stats['W'].values[0] * team1_stats['GF'].values[0] * team2_stats['L'].values[0] *
             team2_stats['GA'].values[0] * team1_goals_scored.mean() * team2_goals_conceded.mean())
        )
        print(team1_stats, team2_stats, team1_likelihood, team2_likelihood, team1_goals_scored, team2_goals_scored)
        return team1_likelihood * 100, team2_likelihood * 100

    except IndexError:
        return np.nan, np.nan


if __name__ == '__main__':
    open_game_data()
