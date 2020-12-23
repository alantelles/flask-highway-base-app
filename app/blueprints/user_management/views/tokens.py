from app import db
from flask import request
from app.blueprints.user_management.models.token import Token
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role

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

    def authenticate(self):
        # only accepts JSON
        body =  request.get_json()
        user = User.authenticate(body['username'], body['password'])
        if user:
            token = Token(user_id=user.id)
            token.create()
            db.session.add(token)
            db.session.commit()
            roles_ids = [r.role_id for r in user.roles]
            user_roles = db.session.query(Role).filter(Role.id.in_(roles_ids)).all()
            user_roles = Role.serialize_list(user_roles)
            user.user_roles = [r['name'] for r in user_roles]
            return {
                'access_token': token.access,
                'refresh_token': token.refresh_token,
                'access_token_expires_in_minutes': token.access_time,
                'refresh_token_expires_in_days': token.refresh_time,
                'user': user.to_json()
            }

    def authorize(self):
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