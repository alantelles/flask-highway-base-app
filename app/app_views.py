# Core app views. You probably won't have to modify this

from flask import render_template, request, session, redirect, url_for, g, flash

from app import app
from app.blueprints.user_management.views.access_control import try_login_user, logout_user, must_be_logged

class App:
    @must_be_logged
    def index(self):
        return render_template('index.html')


    def login(self):
        if g.access.is_anonymous:
            return render_template("application/login.html")

        else:
            flash('Already logged. Redirecting to index', 'info')
            return redirect(url_for('index'))

    def login_try(self):
        return try_login_user(request.form)

    @must_be_logged
    def logout(self):
        return logout_user()

app_views = App()

app.add_url_rule('/', 'index', app_views.index)
app.add_url_rule('/login', 'login', app_views.login, methods=['GET'])
app.add_url_rule('/login', 'login_try', app_views.login_try, methods=['POST'])
app.add_url_rule('/logout', 'logout', app_views.logout, methods=['GET', 'POST'])