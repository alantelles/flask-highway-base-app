from app import db
from datetime import datetime

class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=None, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime(), default=None)