from flask import render_template, redirect, request,url_for
from app import db
from app.blueprints.user_management.models.role import Role

class RolesViews:
    def index(self):
        roles = Role.query.all()
        return render_template('user_management/roles/index.html', roles=roles)

    def create(self):
        name = request.form['name']
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('user_management.roles.show', id=role.id))

    def new(self):
        return render_template('user_management/roles/new.html')

    def show(self, id):
        role = Role.query.filter_by(id=id).first()
        return render_template('user_management/roles/show.html', role=role)

roles_views = RolesViews()