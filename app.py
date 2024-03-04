from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import text

server = 'tehpod'
database = 'Carts'
username = 'sa'
password = 'Qq123456'
driver = 'ODBC Driver 17 for SQL Server'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)


class Cartriges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cartrige = db.Column(db.String(50), nullable=False)
    printer = db.Column(db.String(50), nullable=False)
    fio = db.Column(db.String(50), nullable=True)
    receive_date = db.Column(db.DateTime, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    received = db.Column(db.Integer, nullable=True)
    released = db.Column(db.Integer, nullable=True)
    plan = db.Column(db.Integer, nullable=False)
    fact = db.Column(db.Integer, nullable=True)
    month_rate = db.Column(db.Integer, nullable=True)
    total_rate = db.Column(db.Integer, nullable=True)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/card-auth', methods=['POST', 'GET'])
def card_auth():
    if request.method == 'POST':
        card_number = request.form['card_number']
        print(card_number)

        try:
            card_from_db = db.session.query(Users).filter(Users.card_number == card_number).first()
            user_from_db = card_from_db.name
            print(user_from_db)
            return render_template('cartriges.html')
        except:
            return render_template('auth-fail.html')

    return render_template('card-auth.html')


@app.route('/pass-auth')
def pass_auth():
    return render_template('pass-auth.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/cartriges')
def cartriges():
    return render_template('cartriges.html')



if __name__ == '__main__':
    app.run(debug=True)