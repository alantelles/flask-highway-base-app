import os
from flask import Blueprint, render_template, request

user_management = Blueprint('user_management', __name__, template_folder='templates')
user_management_path = os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management')


class UserManagementViews:
    def index(self):
        controllers_list = os.listdir(os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management', 'views'))
        filtered = [filt for filt in controllers_list if not filt.startswith('__')]
        return render_template("user_management/index.html", views=filtered)

user_management_views = UserManagementViews()

