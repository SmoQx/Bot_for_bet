from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def display_csv():
    with open('table_data0.csv', 'r') as file:
        csv_data = list(csv.reader(file))

    return render_template('index.html', csv_data=csv_data)


if __name__ == '__main__':
    app.run(debug=True)
