import os
from flask import render_template, request

def render(fn):
    def wrapper(self, *args, **kwargs):
        
        proc_path = os.path.join(*request.endpoint.split('.'))
        template_file = f'{proc_path}.html'
        resp = fn(self, *args, **kwargs)
        dump = self.__dict__
        if not resp:
            return render_template(template_file, **dump)

        else:
            return resp

    return wrapper



class CoreViews:
    def render(self, path):
        dump = self.__dict__
        obj = str(self)
        obj = obj[1:obj.rfind('.')].split('.')
        local = [obj[2], obj[4]]
        path = path.split(os.path.sep)
        
        return render_template(os.path.join('user_management', 'roles','index.html'), **dump)