from flask import render_template, redirect, request, url_for, session, flash
import app.blueprints.user_management.views.access_control as access_control

class PocsViews:
    def index(self):
        return 'returning index'

    def show(self, id):
        return f'returning show: {id}'

    def new(self):
        return 'returning new'

    def create(self):
        return 'returning create'

    def update(self, id):
        return f'returning update: {id}'

    def destroy(self, id):
        return f'returning destroy: {id}'

    def edit(self, id):
        return f'returning edit: {id}'

    def see_this(self, id):
        return f'returnin see: {id}'

pocs_views = PocsViews()