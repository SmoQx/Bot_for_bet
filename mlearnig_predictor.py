import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Load data from CSV file
data = pd.read_csv('football_data.csv')

# Split data into training and test sets
train_data, test_data, train_labels, test_labels = train_test_split(
    data.drop('outcome', axis=1),
    data['outcome'],
    test_size=0.2,
    random_state=42
)

# Train random forest classifier
model = RandomForestClassifier()
model.fit(train_data, train_labels)

# Define input data for prediction
new_data = pd.DataFrame({
    'team1_games_played': [3],
    'team1_wins': [2],
    'team1_player_quality': [9],
    'team1_injured_players': [7],
    'team2_games_played': [12],
    'team2_wins': [9],
    'team2_player_quality': [8],
    'team2_injured_players': [1],
})

# Predict outcome of new data
prediction = model.predict_proba(new_data)[0]

# Print predicted outcome in percentages
team1_name = 'Team XYZ'
team2_name = 'Team ZYX'
print(f'{team1_name} {prediction[0]*100:.2f}% vs {team2_name} {prediction[1]*100:.2f}%')
print(prediction)
