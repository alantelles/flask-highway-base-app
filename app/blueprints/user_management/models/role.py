from app import db
from app.dont_touch.models_mixins import BaseModel
from app.blueprints.user_management.models.user_role import UserRole

class Role(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default='normal', unique=True)
    users = db.relationship('UserRole', back_populates='role')
