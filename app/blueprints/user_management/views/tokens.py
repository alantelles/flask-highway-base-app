from app import db
from flask import request
from app.blueprints.user_management.models.token import Token

class TokensViews():
    def index(self):
        tokens = Token.query.all()
        tks = Token.serialize_list(tokens)
        return {'data': tks}
        
    def create(self, user_id):
        token = Token()
        token.create()
        db.session.add(token)
        db.session.commit()
        return 'token created'

    def auth(self):
        token_try = request.headers.get('Authorization')
        token_try = token_try.replace('Bearer ', '')
        token = Token()
        found = token.validate(token_try)
        return f'Token {token_try} authenticated? {found}'

    def refresh(self):
        token_try = request.headers.get('Authorization')
        token_try = token_try.replace('Bearer ', '')
        token = Token.query.filter_by(refresh_token=token_try).first()
        if token.refresh():
            db.session.commit()
        
        return f'Token {token_try} renewed? {token}'
        

        

tokens_views = TokensViews()