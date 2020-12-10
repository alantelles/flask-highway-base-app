from flask import request, session, redirect, url_for
from app import app

admin_role_name = app.config.get('ADMIN_ROLE_NAME', 'admien')

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
        if 'admin' == admin_role_name:
            return fn(self, *args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper