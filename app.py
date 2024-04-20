from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus as url_quote
import os
import  testGEnai 

import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.urandom(24)

API_KEY = "YOUR_API_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get("message")
        print(user_message)  # For debugging
        bot_response = testGEnai.respond(user_message)
        return jsonify({'bot_response': bot_response})
    else:
        return render_template('chat.html')  # If it's a GET request, render the chat template without any bot response


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error_message='Email already exists. Please use a different email.')

        password = request.form['password']
        hashed_password = generate_password_hash(password)

        name = request.form.get('name', '')
        age = request.form.get('age', None)

        new_user = User(email=email, password=hashed_password, name=name, age=age)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('signin.html', error_message=error_message)

    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)
