import yaml

from app import app
from app.helpers import register_routes

#DON'T REMOVE: blueprints register section
# import app.blueprints.user_management.views.users as users_views
from app.blueprints.user_management import user_management_views
from app.blueprints.user_management.views.users import users_views
from app.blueprints.user_management.views.roles import roles_views
#END: blueprints register section

URL_PREFIX = '/user_management'
print(f'Registering routes for {URL_PREFIX}')
app.add_url_rule(f'{URL_PREFIX}/', 'user_management_views.index', user_management_views.index, methods=['GET'])

register_routes(
    'user_management', 
    users=users_views, 
    roles=roles_views, 
    user_management_views=user_management_views
)

"""
app.add_url_rule(f'{URL_PREFIX}/users/', 'user_management.users.index', users_views.index, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/users/<id>/', 'user_management.users.show', users_views.show, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/users/new/', 'user_management.users.new', users_views.new, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/users/new/', 'user_management.users.create', users_views.create, methods=['POST'])
"""

app.add_url_rule(f'{URL_PREFIX}/roles/', 'user_management.roles.index', roles_views.index, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/roles/<id>/', 'user_management.roles.show', roles_views.show, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/roles/new/', 'user_management.roles.new', roles_views.new, methods=['GET'])
app.add_url_rule(f'{URL_PREFIX}/roles/new/', 'user_management.roles.create', roles_views.create, methods=['POST'])
