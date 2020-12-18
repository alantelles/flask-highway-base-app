from app import db
from app.models_mixins import TimeStampMixin, Serializer, Desserializer
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.audit import Audit
from app.blueprints.user_management.models.user_role import UserRole
from werkzeug.security import generate_password_hash, check_password_hash


def to_upper(arg):
    return arg.upper()

def format_date(arg):
    return arg.strftime("%d/%m/%Y %H:%M:%S")

class User(db.Model, TimeStampMixin, Serializer, Desserializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    audits = db.relationship('Audit')
    password_hash = db.Column(db.String(255), unique=True)
    roles = db.relationship('UserRole', back_populates='user')

    forbidden_fields = ['password_hash']
    remap = {'user_roles': 'roles'}
    process_key = {
        'name': to_upper,
        'created_at': format_date
    }
    
    accept_only = ['name', 'username']
    
    process_input_key = {'password_hash': generate_password_hash}
    remap_input = {'password': 'password_hash'}
    

    def set_password(pw):
        return generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)