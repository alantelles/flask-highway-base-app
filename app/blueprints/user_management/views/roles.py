from flask import render_template, redirect, request, url_for, session, flash
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
        session['now_viewed'] = id
        role = Role.query.filter_by(id=id).first()
        
        return render_template('user_management/roles/show.html', role=role)

    def edit(self, id):
        session['now_edited'] = id
        role = Role.query.get(id)
        return render_template('user_management/roles/edit.html', role=role)

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

    def destroy(self, id):
        try:
            if session.get('now_viewed', None) == id:
                role = Role.query.filter_by(id=id)
                role.first().users = []
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
            print(e)
            return {
                'message': 'Nothing happened', 
                'redirect': url_for('user_management.roles.show', id=id)
            }, 500

roles_views = RolesViews()