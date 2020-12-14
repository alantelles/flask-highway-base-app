from app import db
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.user_roles import user_roles

try:
    print('Creating database')
    db.create_all()
    db.session.commit()
except Exception as e:
    print(f"Tables not created because: {e}")
print('Adding admin role')

from app import app as flask_app
admin_role = Role(name=flask_app.config.get('ADMIN_ROLE_NAME', 'admin'))
db.session.add(admin_role)
db.session.commit()
print('Admin role added succesfully')
print('Adding admin user')
admin_user = User(name='Administrator', username='admin', password_hash=User.set_password('admin123'))
admin_user.roles.append(admin_role)
db.session.commit()
print('Admin user added succesfully')