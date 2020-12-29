from app import db
from app.base_model import BaseModel

class UserRole(db.Model, BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    user = db.relationship("User", back_populates="roles")
    role = db.relationship("Role", back_populates="users")

    forbidden_fields = ['role']