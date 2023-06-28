from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from mlearning_skilearn import calculate_likelihood
from data_reader import does_exist

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route("/")
def display_csv():
    return render_template('index.html')


@app.route('/wynik', methods=['POST'])
def redirect_page():
    team1 = request.form['team1']
    team2 = request.form['team2']
    value1, value2 = calculate_likelihood(team1, team2)
    """print(value1, value2)
    value1, value2 = str(value1), str(value2)"""
    return redirect(url_for('another_page', team1=f'{team1} {value1}%', team2=f'{team2} {value2}%'))


@app.route('/wynik')
def another_page():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    return render_template('/wynik_mecz.html', team1=team1, team2=team2)


if __name__ == '__main__':
    does_exist()
    app.run(debug=True)
