from app import db
from flask import request
from app.blueprints.user_management.views.audits import audited
from app.blueprints.user_management.models.token import Token
from app.blueprints.user_management.models.user import User
from app.blueprints.user_management.models.role import Role

class TokensViews():
    def index(self):
        tokens = Token.query.all()
        tks = Token.serialize_list(tokens)
        return {'data': tks}

    @audited('This view revokes all tokens')
    def revoke_all(self):
        # temporary code for tests purpose
        # should be decorated
        dels = Token.revoke_all()
        db.session.commit()
        return {'deleted': dels}
        
    
    def get_user_data(user):
        roles_ids = [r.role_id for r in user.roles]
        user_roles = db.session.query(Role).filter(Role.id.in_(roles_ids)).all()
        user_roles = Role.serialize_list(user_roles)
        user.user_roles = [r['name'] for r in user_roles]
        return user

    @audited('This view authenticates an user and creates an access token')
    def authenticate(self):
        # only accepts JSON
        body =  request.get_json()
        user = User.authenticate(body['username'], body['password'])
        if user:
            token = Token(user_id=user.id)
            token.create()
            db.session.add(token)
            db.session.commit()
            user_retrieved = TokensViews.get_user_data(user)

            return {
                'access_token': token.access,
                'refresh_token': token.refresh_token,
                'access_token_expires_in_minutes': token.access_time,
                'refresh_token_expires_in_days': token.refresh_time,
                'user': user_retrieved.to_json()
            }

        else:
            return {'message': 'Invalid credentials'}, 401

    @audited('This view authorizes an user with a valid token previously registered')
    def authorize(self):
        token_try = request.headers.get('Authorization')
        token_try = token_try.replace('Bearer ', '').strip()
        token = Token()
        found = token.validate(token_try)
        if found:
            user = User.query.filter_by(id=found.user_id).first()
            if user:
                user_retrieved = TokensViews.get_user_data(user)
                return {
                    'message': 'Valid token. Access granted',
                    'user': user_retrieved.to_json()
                }, 200

            else:
                return {'message': 'Your token seems valid, but the associated user has no access anymore'}, 401

        else:
            return {'message': 'Invalid token. Try refreshing or authenticate again.'}, 401
        
    @audited('This view refreshes an access token for a given refresh token')
    def refresh(self):
        token_try = request.headers.get('Authorization')
        token_try = token_try.replace('Bearer ', '')
        token = Token.query.filter_by(refresh_token=token_try).first()
        if token:
            if token.refresh(token_try):
                db.session.commit()
                return {
                    'access_token': token.access,
                    'refresh_token': token.refresh_token,
                    'access_token_expires_in_minutes': token.access_time,
                    'refresh_token_expires_in_days': token.refresh_time
                }
        
        return {'message': 'Invalid refresh token'}, 401
        

        

tokens_views = TokensViews()