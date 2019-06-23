import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Signal


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            name = request.form['name']
            unit = request.form['unit']
            fs = request.form['fs']
            try:
                signal = Signal(
                    name=name,
                    unit=unit,
                    fs=fs
                )
                db.session.add(signal)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
        except:
            errors.append(
                "Unable to create signal"
            )
    return render_template('index.html', errors=errors)


if __name__ == '__main__':
    app.run()