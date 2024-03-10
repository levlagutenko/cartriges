from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, UserMixin, login_user
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
app.secret_key = 'Qq23514789'
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
            return redirect('/cartriges')
        except:
            return render_template('auth-fail.html')
    return render_template('card-auth.html')


@app.route('/pass-auth', methods=['POST', 'GET'])
def pass_auth():
    if request.method == 'POST':
        user_pass = request.form['pass']
        print(user_pass)
        try:
            pass_from_db = db.session.query(Users).filter(Users.password == user_pass).first()
            user_from_db = pass_from_db.name
            print(user_from_db)
            return redirect('/cartriges')
        except:
            return render_template('auth-fail.html')
    return render_template('pass-auth.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        reg_name = request.form['reg_name']
        reg_surname = request.form['reg_surname']
        reg_password = request.form['reg_password']
        reg_passwordconfirm = request.form['reg_passwordconfirm']
        reg_cardnumber = request.form['reg_cardnumber']

        if not reg_name or not reg_surname or not reg_password or not reg_cardnumber:   #### Проверка на обязательные поля
            flash('Заполните обязательные поля', 'error')
            return redirect('/registration')

        elif reg_password != reg_passwordconfirm:   #### Проверка на совпадения пароля и подтверждения
            flash('Пароль и подтверждение не совпадают', 'error')
            return redirect('/registration')

        reg_user_name = reg_name + ' ' + reg_surname    #### Складываем имя и фамилию для добавления в базу

        try:
            new_user = Users(name=reg_user_name, password=reg_password, card_number=reg_cardnumber) #### Добавляем нового пользователя в базу
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация выполнена', 'succes')
            return redirect('/index')
        except:
            return render_template('reg-fail.html')
    return render_template('registration.html')

@app.route('/cartriges', methods=['POST', 'GET'])
def cartriges():

    cartriges = db.session.query(Cartriges.cartrige).all() #### Выбираем все картриджи из БД для добавления в комбобокс

    return render_template('cartriges.html', cartriges=cartriges)


if __name__ == '__main__':
    app.run(debug=True, host='444-444', port=5000)