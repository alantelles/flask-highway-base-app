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

    def revoke_all():
        dels = Token.query.delete()
        return dels
    
    def validate(self, code):        
        found = Token.query.filter_by(access=code).first()
        if found:
            now = datetime.now()
            if not found.updated_at:
                ref_time = found.created_at

            else:
                ref_time = found.updated_at

            elapsed = now - ref_time
            elapsed_min = elapsed.seconds / 60
            if elapsed_min <= found.access_time:
                return found
                
            else:
                return False
        else:
            return False
            
    def refresh(self, code):
        now = datetime.now()
        elapsed = now - self.created_at

        if elapsed.days <= self.refresh_time:
            self.access = sc.token_urlsafe(64)
            return True

        else:
            return False
            
    
    def create(self, at=60, rt=2):
        self.access = sc.token_urlsafe(64)
        self.refresh_token = sc.token_urlsafe(64)
        self.access_time = at
        self.refresh_time = rt