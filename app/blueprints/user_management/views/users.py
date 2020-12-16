from flask import render_template, request, redirect, url_for, session, flash
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.user_role import UserRole
from app import db
from app.blueprints.user_management.views.access_control import only_admin

class UsersViews:

    @only_admin
    def index(self):
        users = User.query.all()
        return render_template('user_management/users/index.html', users=users)
    
    @only_admin
    def show(self, id):
        session['now_viewed'] = id
        user = User.query.filter_by(id=id).first()
        return render_template('user_management/users/show.html', user=user)

    @only_admin
    def new(self):
        roles = Role.query.all()
        user = User(username='', name='')
        return render_template('user_management/users/new.html', roles=roles, user=user)
   
    @only_admin
    def edit(self, id):
        session['now_edited'] = id
        roles = Role.query.all()
        user = User.query.get(id)
        user_roles_ids = [r.role_id for r in user.roles]
        return render_template('user_management/users/edit.html', roles=roles, user=user, user_roles_ids=user_roles_ids)

    @only_admin
    def update(self, id):
        if session.get('now_edited', None) == id:
            user = User.query.get(id)
            user.name = request.form['name']
            user.username = request.form['username']
            roles_ids = [int(id) for id in request.form.getlist('roles')]
            if len(roles_ids):
                user_roles = UserRole.query.filter_by(user_id=user.id).all()
                for ur in user_roles:
                    if ur.role.id not in roles_ids:
                        UserRole.query.filter_by(user_id=ur.user_id, role_id=ur.role_id).delete()
                

                roles = db.session.query(Role).filter(Role.id.in_(roles_ids)).all()
                for r in roles:
                    print(r)
                    print(user.roles)
                    print(r in user.roles)
                    user_roles_ids = [r.role_id for r in user.roles]
                    if r.id not in user_roles_ids:
                        assoc = UserRole()
                        assoc.role = r
                        assoc.user = user
                        db.session.add(assoc)

            else:
                UserRole.query.filter_by(user_id=user.id).delete()

            db.session.commit()
            flash(f'User {user.name} edited successfully', 'success')
            return redirect(url_for('user_management.users.show', id=id))
        else:
            flash('Irregular editing try refused', 'error')
            return redirect(url_for('user_management.users.index')), 400

    @only_admin
    def create(self):
        post_data = request.form
        roles_ids = [int(id) for id in request.form.getlist('roles')]
        user = User(
                name=post_data['name'],
                username=post_data['username'],
                password_hash=User.set_password(post_data['password'])
            )
        if len(roles_ids):
            roles = db.session.query(Role).filter(Role.id.in_(roles_ids)).all()
            
            
            for r in roles:
                assoc = UserRole()
                assoc.role = r
                user.roles.append(assoc)
                db.session.add(assoc)

            

        else:
            db.session.add(user)

        db.session.commit()
        return redirect(url_for('user_management.users.show', id=user.id))

    @only_admin
    def destroy(self, id):
        try:
            if session.get('now_viewed', None) == id:
                user = User.query.filter_by(id=id)
                user_roles = UserRole.query.filter_by(user_id=user.first().id)
                user_roles.delete()
                name = user.first().name
                user.delete()
                db.session.commit()
                flash(f'User {name} deleted successfully', 'success')
                return {
                    'message': f'User {name} has been deleted', 
                    'redirect': url_for('user_management.users.index')
                }, 200

            else:
                return {
                    'message': f'Irregular deleting try',
                    'redirect': url_for('user_management.users.index')
                }, 400

        except Exception as e:
            print(e)
            return {
                'message': 'Nothing happened', 
                'redirect': url_for('user_management.users.show', id=id)
            }, 500
    
users_views = UsersViews()