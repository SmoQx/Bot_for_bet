from flask import Flask, render_template, url_for, redirect
import csv

app = Flask(__name__)


@app.route("/")
def display_csv():
    return render_template('index.html')


@app.route('/wynik', methods=['POST'])
def redirect_page():
    return redirect(url_for('another_page'))


@app.route('/wynik')
def another_page():
    return render_template('/wynik_mecz.html')


if __name__ == '__main__':
    app.run(debug=True)
