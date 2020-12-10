import os
from app import app

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#session and security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'some-random-secret-key')
app.config['ADMIN_ROLE_NAME'] = 'admin'

#others
app.config['EXPLAIN_TEMPLATE_LOADING'] = False
app.config['project_name'] = 'Flask Highway'