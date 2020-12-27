# Core app views. You probably won't have to modify this

from flask import render_template, request, session, redirect, url_for, g, flash

from app.views.base_views import BaseViews
from app import app
from app.blueprints.user_management.views.access_control import try_login_user, logout_user, must_be_logged


class DefaultViews(BaseViews):
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

    def site_map(self):
        urls = []
        for r in app.url_map.iter_rules():
            urls.append({
                'route': r.rule,
                'methods': list(r.methods),
                'view': r.endpoint,
                'defaults': r.defaults
            })

        return {'urls': urls}
        

    @must_be_logged
    def logout(self):
        return logout_user()

default_views = DefaultViews()

app.add_url_rule('/', 'index', default_views.index)
app.add_url_rule('/login', 'login', default_views.login, methods=['GET'])
app.add_url_rule('/login', 'login_try', default_views.login_try, methods=['POST'])
app.add_url_rule('/logout', 'logout', default_views.logout, methods=['GET', 'POST'])
app.add_url_rule('/site_map', 'site_map', default_views.site_map, methods=['GET'])