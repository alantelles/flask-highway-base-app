import traceback
from flask import render_template, redirect, request, url_for, session, flash
from app import db
from app.views.base_views import BaseViews
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.audit import Audit
from app.blueprints.user_management.models.user_role import UserRole
from app.blueprints.user_management.views.access_control import only_admin

from dont_touch.core_views import render

class RolesViews(BaseViews):
    
    @only_admin
    def index(self):
        self.roles = Role.query.all()
        return self.render('index')

    @only_admin
    def create(self):
        name = request.form['name']
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('user_management.roles.show', id=role.id))

    @only_admin
    def new(self):
        return self.render('new')

    @only_admin
    def show(self, id):
        session['now_viewed'] = id
        role = Role.query.filter_by(id=id).first()
        
        return render_template('user_management/roles/show.html', role=role)

    @only_admin
    def edit(self, id):
        session['now_edited'] = id
        role = Role.query.get(id)
        return render_template('user_management/roles/edit.html', role=role)

    @only_admin
    def update(self, id):
        if session.get('now_edited', None) == id:
            role = Role.query.get(id)
            role.name = request.form['name']
            db.session.commit()
            flash(f'Role {role.name} edited successfully', 'success')
            return redirect(url_for('user_management.roles.show', id=id))
        else:
            flash('Irregular editing try refused', 'error')
            return redirect(url_for('user_management.roles.index')), 400

    @only_admin
    def destroy(self, id):
        try:
            if session.get('now_viewed', None) == id:
                role = Role.query.filter_by(id=id)
                role.users = []
                user_roles = UserRole.query.filter_by(role_id=role.first().id)
                user_roles.delete()
                name = role.first().name
                role.delete()
                db.session.commit()
                flash(f'Role {name} deleted successfully', 'success')
                return {
                    'message': f'Role {name} has been deleted', 
                    'redirect': url_for('user_management.roles.index')
                }, 200

            else:
                return {
                    'message': f'Irregular deleting try',
                    'redirect': url_for('user_management.roles.index')
                }, 400

        except Exception as e:
            traceback.print_exc()
            flash(f'An error occurred!', 'danger')
            return {
                'message': 'Nothing happened', 
                'redirect': url_for('user_management.roles.show', id=id)
            }, 500

roles_views = RolesViews()