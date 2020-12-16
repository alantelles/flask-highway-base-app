from app import db
from app.models_mixins import TimeStampMixin, SerializeOutput
from app.blueprints.user_management.models.user_role import UserRole

class Role(db.Model, TimeStampMixin, SerializeOutput):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default='normal', unique=True)
    users = db.relationship('UserRole', back_populates='role')
