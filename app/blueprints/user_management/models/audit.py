from app import db
from app.models_mixins import BaseModel

class Audit(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    view = db.Column(db.String(255))
    route = db.Column(db.String(255))
    query_string = db.Column(db.String(255))
    body = db.Column(db.Text)
    headers = db.Column(db.Text)
    description = db.Column(db.String(255))
