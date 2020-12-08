from flask import render_template, request, redirect, url_for
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role
from app import db

def index():
    users = User.query.all()
    return render_template('user_management/users/index.html', users=users)

def show(id):
    return render_template('user_management/users/show.html')

def new():
    roles = Role.query.all()
    return render_template('user_management/users/new.html', roles=roles)

def create():
    post_data = request.form
    roles = request.form.getlist('roles')
    user = User(
        name=post_data['name'],
        username=post_data['username'],
        password_hash=User.set_password(post_data['password']),
        roles=roles
    )
    print(user)
    return 'saved'