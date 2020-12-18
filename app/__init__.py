from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__main__)

from app import config

db = SQLAlchemy(app)

from app import app_views 

@app.context_processor
def inject_dict_for_all_templates():
    return dict(go_away='go away string')

#DON'T REMOVE: blueprints register section
from app.blueprints.user_management import user_management
app.register_blueprint(user_management)
#END: blueprints register section

