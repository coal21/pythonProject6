from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text


app = Flask(__name__)

conn_str = "mysql://root:simplepassword@localhost/StoreDB"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/', methods=['POST', 'GET'])
def create_reg():
    if request.method == 'POST':
        email = request.form['Email']
        username = request.form['username']
        password = request.form['Password']
        Job = request.form.get('Job')
        conn.execute(text(
            'INSERT INTO Users (Email, Username, Password, Job) VALUES (:email, :username, :password, :Job)'),
                {'email': email, 'username': username, 'password': password, 'Job': Job})
        conn.commit()
        return render_template('index.html', username=username)
    else:
        return render_template('Register.html')

import logging
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        logging.info(f"User login attempt with email: {email}, password: {password}")

        result = conn.execute(text(
            'SELECT * FROM Users WHERE Email = :email AND Password = :password'),
            {'email': email, 'password': password})
        user = result.fetchone()

        if user:
            return render_template('index.html', username=user['Username'])
        else:
            return render_template('login.html', error="Invalid email or password")
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)