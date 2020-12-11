from flask import render_template, request, session, redirect, url_for

from app import app
from app.blueprints.user_management.views.access_control import try_login_user, logout_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template("application/login.html")

@app.route('/login', methods=['POST'])
def login_try():
    return try_login_user(request.form)

@app.route('/logout', methods=['GET'])
def logout():
    return logout_user()
