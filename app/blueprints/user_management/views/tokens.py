from app import db
from app.blueprints.user_management.models.token import Token

class TokensViews():
    def index(self):
        tokens = Token.query.all()
        tks = Token.serialize_list(tokens)
        return {'data': tks}
        
    def create(self):
        token = Token()
        token.create()
        db.session.add(token)
        db.session.commit()
        return 'token created'
        
tokens_views = TokensViews()