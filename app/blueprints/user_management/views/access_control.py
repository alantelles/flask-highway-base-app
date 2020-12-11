from flask import request, session, redirect, url_for, flash, g
from app import app
from app.blueprints.user_management.models.user import User

admin_role_name = app.config.get('ADMIN_ROLE_NAME', 'admin')

def roles_allowed(role_list):
    def decorator(fn):
        def wrapper(self, *args):
            
            ok = 'admin'
            if ok in role_list:
                return fn(self, *args)
            else:
                return redirect(url_for('login'))

        return wrapper
    return decorator
        

def only_admin(fn):
    def wrapper(self, *args, **kwargs):
        print("only admin can view this")
        logged = g.access.user
        if logged:
            if g.access.is_admin:
                return fn(self, *args, **kwargs)
            else:
                flash('This page is only allowed to system administrator', 'info')
                return redirect(url_for('login'))
        else:
            flash('This page is only allowed to system administrator', 'info')
            return redirect(url_for('login'))

    return wrapper

def must_be_logged(fn):
    def wrapper(self, *args, **kwargs):
        
        logged = g.access.user
        print(logged)
        if logged:
            return fn(self, *args, **kwargs)

        else:
            print("passei aqui")
            flash('You must be logged to see this page', 'info')
            return redirect(url_for('login'))

    return wrapper

def try_login_user(form_data):
    user = User.query.filter_by(username=form_data['username']).first()

    if user.check_password(form_data['password']):
        #
        session['logged_user'] = user.id
        return redirect(url_for('index'))

    else:
        flash("Invalid credentials. Can't log you in.", "danger")
        return redirect(url_for('login'))

def logout_user():
    session['logged_user'] = None
    print('Logging user out')
    g.access = AccessController()
    flash('You were logged out', 'info')
    return redirect(url_for('login'))

class AccessController:
    def __init__(self):
        self.is_anonymous = True
        self.is_admin = None
        self.roles = None
        self.roles_names = None
        self.user = None
        
    def setup_user(self):
        
        user_id = session.get('logged_user')
        if user_id:
            user = User.query.get(user_id)
            if user:
                self.user = user
                self.roles = [role.id for role in user.roles]
                self.roles_names = [role.name for role in user.roles]
                self.is_anonymous = False
                self.is_admin = admin_role_name in self.roles_names
        
@app.before_request
def set_access_controller_helper():
    g.access = AccessController()
    g.access.setup_user()

@app.context_processor
def session_helpers():
    
    return dict(
            access=g.access
        )