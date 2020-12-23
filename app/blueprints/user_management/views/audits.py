import json
from flask import render_template, session, request
from app import db
from app.blueprints.user_management.models.audit import Audit
from app.blueprints.user_management.models.token import Token

def audited(description):
    def decorator(fn, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            h_dict = {}
            for k in request.headers:
                h_dict[k[0].lower()] = request.headers[k[0]]

            user_id = session.get('logged_user', None)
            authorization = request.headers.get('Authorization', None)
            if authorization:
                token_str = authorization.replace('Bearer ', '').strip()
                user_id = Token.find_user(token_str)


            audit = Audit(
                user_id=user_id, 
                authorization=authorization,
                view=request.endpoint,
                route=request.path,
                description=description,
                query_string=request.query_string.decode(),
                body=request.get_data().decode(),
                headers=json.dumps(h_dict)
            )
            db.session.add(audit)
            db.session.commit()
            return fn(self, *args, **kwargs)

        return wrapper

    return decorator

class AuditsViews:
    def index(self):
        audits = Audit.query.all()
        keys = [key for key in Audit.__dict__ if not key.startswith('_')]
        return render_template('user_management/audits/index.html', audits=audits, keys=keys, getattr=getattr)

    def search(self):
        term = request.args.get('view_name')
        audits = Audit.query.filter(Audit.view.like(f'%{term}%')).all()
        keys = [key for key in Audit.__dict__ if not key.startswith('_')]
        return render_template('user_management/audits/index.html', audits=audits, keys=keys, getattr=getattr, view_name=term)

audits_views = AuditsViews()