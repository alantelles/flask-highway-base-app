from app import db
import secrets as sc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.dont_touch.models_mixins import BaseModel

class Token(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    refresh_token = db.Column(db.String(255))
    access_time = db.Column(db.Integer) # in minutes
    refresh_time = db.Column(db.Integer) # in days
    access = db.Column(db.String(255))
    
    def validate(self, code):        
        found = Token.query.filter_by(access=code).first()
        if found:
            now = datetime.now()
            elapsed = now - found.created_at
            elapsed_min = elapsed.seconds / 60
            if elapsed_min < found.access_time:
                return True
                
            else:
                return False
        else:
            return False
            
    def refresh(self, code):
        now = datetime.now()
        elapsed = now - found.created_at

        if elapsed.days < found.refresh_time:
            self.access = sc.token_urlsafe(64)
            return True

        else:
            return False
            
    
    def create(self, at=60, rt=2):
        self.access = sc.token_urlsafe(64)
        self.refresh_token = sc.token_urlsafe(64)
        self.access_time = at
        self.refresh_time = rt