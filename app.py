import numpy as np
import pandas as pd
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from mlearning_skilearn import calculate_likelihood
from data_reader import does_exist, check_values
from pathlib import Path
import re


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predit.db'
db = SQLAlchemy(app)


class TeamData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(200))
    team2 = db.Column(db.String(200))
    score1 = db.Column(db.String(200))
    score2 = db.Column(db.String(200))


class ChampionshipData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Team = db.Column(db.String(200))
    GP = db.Column(db.String(200))
    W = db.Column(db.String(200))
    D = db.Column(db.String(200))
    L = db.Column(db.String(200))
    GF = db.Column(db.String(200))
    GA = db.Column(db.String(200))
    GD = db.Column(db.String(200))
    PPG = db.Column(db.String(200))
    CS = db.Column(db.String(200))
    FTS = db.Column(db.String(200))


class GameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Team1 = db.Column(db.String(200))
    Score = db.Column(db.String(200))
    Team2 = db.Column(db.String(200))


@app.route("/")
def display_csv():
    return render_template('index.html')


@app.route('/wynik', methods=['POST'])
def redirect_page():
    team1 = request.form['team1']
    team2 = request.form['team2']
    value1, value2 = calculate_likelihood(team1, team2)

    new_game_pred = TeamData(team1=team1, team2=team2, score1=value1, score2=value2)

    db.session.add(new_game_pred)
    db.session.commit()
    print(TeamData.query.order_by(TeamData.id).all())

    return redirect(url_for('another_page', team1=f'{team1} {value1: .2f}%', team2=f'{team2} {value2: .2f}%'))


@app.route('/wynik')
def another_page():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    return render_template('/wynik_mecz.html', team1=team1, team2=team2)


@app.route("/import-championship-data")
def import_championship_data():
    # Read the CSV file into a pandas DataFrame
    pattern = r'football_data\d+.csv'
    dir_path = Path.cwd()
    direcories = [direcory for direcory in dir_path.iterdir() if re.search(pattern, str(direcory))]
    merger = pd.concat([pd.read_csv(dir_name) for dir_name in direcories])
    df_championship = merger

    # Delete existing data in the ChampionshipData table
    db.session.query(ChampionshipData).delete()
    db.session.commit()

    # Import DataFrame to the ChampionshipData table
    df_championship.to_sql('championship_data', con=db.engine, if_exists='append', index=False)

    return 'Championship data imported successfully!'


@app.route("/import-game-data")
def import_game_data():
    # Read the CSV file into a pandas DataFrame
    df_game = pd.read_csv('table_data0.csv')

    # Delete existing data in the GameData table
    db.session.query(GameData).delete()
    db.session.commit()

    # Import DataFrame to the GameData table
    df_game.to_sql('game_data', con=db.engine, if_exists='replace', index=False)


    return 'Game data imported successfully!'


if __name__ == '__main__':
    does_exist()

    app.run(debug=True)
