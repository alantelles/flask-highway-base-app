from app import db
from app.models_mixins import TimeStampMixin

"""
user_roles = db.Table('user_roles', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
"""
class UserRole(db.Model, TimeStampMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    user = db.relationship("User", back_populates="roles")
    role = db.relationship("Role", back_populates="users")