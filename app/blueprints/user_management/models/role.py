from app import db
from app.models_mixins import TimeStampMixin
from app.blueprints.user_management.models.user_roles import user_roles

class Role(db.Model, TimeStampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default='normal', unique=True)
    users = db.relationship('User', secondary=user_roles, backref=db.backref('User'))

    def __repr__(self):
        return self.name