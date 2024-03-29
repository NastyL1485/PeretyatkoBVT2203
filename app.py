import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db", user="postgres", password="nastyalove", host="localhost", port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            if username == "":
                return render_template('login.html', yshib=True)
            password = request.form.get('password')
            if password == "":
                return render_template('login.html', yshib=True)
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 0:
                return render_template('login.html', yshib=True)
            return render_template('account.html', full_name=records[0][1], password=records[0][3], login=records[0][2])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        if name == "":
            return render_template('registration.html', hyl=True)
        login = request.form.get('login')
        if login == "":
            return render_template('registration.html', hyl=True)
        if login:
            cursor.execute('SELECT * FROM service.users')
            rows = cursor.fetchall()
            for row in rows:
                if login == row[2]:
                    return render_template('registration.html', hyl=True)
        password = request.form.get('password')
        if password == "":
            return render_template('registration.html', hyl=True)

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')