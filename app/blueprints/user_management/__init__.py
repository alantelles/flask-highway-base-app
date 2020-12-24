import os
from flask import Blueprint, render_template, request

from dont_touch.helpers.routes import register_routes
from app.views.base_views import BaseViews

#DON'T REMOVE: blueprint views register section
from app.blueprints.user_management.views.tokens import tokens_views
from app.blueprints.user_management.views.users import users_views
from app.blueprints.user_management.views.roles import roles_views
from app.blueprints.user_management.views.audits import audits_views
#END: blueprint views register section

from app.blueprints.user_management.views.access_control import only_admin

user_management = Blueprint('user_management', __name__, template_folder='templates')
user_management_path = os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management')


class UserManagementViews(BaseViews):
    @only_admin
    def index(self):
        controllers_list = os.listdir(os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management', 'views'))
        filtered = [filt for filt in controllers_list if not filt.startswith('__')]
        return render_template("user_management/index.html", views=filtered)

user_management_views = UserManagementViews()

#DON'T TOUCH: register routes section
register_routes('user_management', user_management_views=user_management_views, users=users_views, roles=roles_views, audits=audits_views, tokens=tokens_views)
#END: register routes section