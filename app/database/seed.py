import sys
from app import db

# Database seed script
# This script will declare models for SQLAlchemy create it in database

# DONT'REMOVE: models declare section
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.user_roles import user_roles
#END: models declare section

try:
    print('Creating database')
    db.create_all()
    db.session.commit()
except Exception as e:
    print(f"Tables not created because: {e}")

try:
    if sys.argv[1] == '--admin':
        print('Creating administrator credentials')
        try:
            admin_username = sys.argv[3]

        except IndexError:
            admin_username = 'admin'

        try:
            admin_name = sys.argv[4]

        except IndexError:
            admin_name = 'Administrator'

        try:
            admin_password = sys.argv[2]

        except IndexError:
            admin_password = 'admin123'
    
        from app import app as flask_app
        admin_role_name = flask_app.config.get('ADMIN_ROLE_NAME', 'admin')
        print(f'Adding admin role called "{admin_role_name}"')
        admin_role = Role(name=admin_role_name)
        db.session.add(admin_role)
        db.session.commit()
        print('Admin role added succesfully')
        print('Adding admin user')
        print('Credentials:')
        print(f'\tName: {admin_name}')
        print(f'\tUsername: {admin_username}')
        print(f'\tPassword: {admin_password}')
        admin_user = User(name=admin_name, username=admin_username, password_hash=User.set_password(admin_password))
        admin_user.roles.append(admin_role)
        db.session.commit()
        print('Administrator user added succesfully')

    else:
        print('Not creating administrator account')

except IndexError:
    print('Not creating administrator account')
    pass

print("Database was created")