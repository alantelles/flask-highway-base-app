from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

from app import config

db = SQLAlchemy(app)

from app.views.default_views import default_views

#DON'T REMOVE: blueprints register section
from app.blueprints.user_management import user_management
app.register_blueprint(user_management)
#END: blueprints register section
