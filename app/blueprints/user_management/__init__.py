import os
from flask import Blueprint, render_template, request

from app.helpers import register_routes

#DON'T REMOVE: blueprint views register section
from app.blueprints.user_management.views.users import users_views
from app.blueprints.user_management.views.roles import roles_views
from app.blueprints.user_management.views.audits import audits_views
from app.blueprints.user_management.views.pocs import pocs_views
#END: blueprint views register section

from app.blueprints.user_management.views.access_control import only_admin

user_management = Blueprint('user_management', __name__, template_folder='templates')
user_management_path = os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management')


class UserManagementViews:
    @only_admin
    def index(self):
        controllers_list = os.listdir(os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management', 'views'))
        filtered = [filt for filt in controllers_list if not filt.startswith('__')]
        return render_template("user_management/index.html", views=filtered)

user_management_views = UserManagementViews()


register_routes('user_management', user_management_views=user_management_views, users=users_views, roles=roles_views, audits=audits_views, pocs=pocs_views)
    