from app import db
from app.models_mixins import TimeStampMixin, SerializeOutput
from app.blueprints.user_management.models.role import Role
from app.blueprints.user_management.models.user_role import UserRole
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, TimeStampMixin, SerializeOutput):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255), unique=True)
    roles = db.relationship('UserRole', back_populates='user')

    forbidden_fields = ['password_hash']
    remap = {'user_roles': 'roles'}
    

    def set_password(pw):
        return generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)