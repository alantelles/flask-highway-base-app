import os
from flask import render_template, redirect, url_for, request

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
    def redirect(self, path, flask_lookup=False):
        dump = dict.copy(self.__dict__)
        print(dump)
        if not flask_lookup:
            obj = str(self)
            obj = obj[1:obj.rfind('.')].split('.')
            # obj = [obj[2], obj[4]]
            path = path.split('.')
            if len(path) == 1:
                to_redir = '.'.join([obj[2], obj[4], path[0]])

            elif len(path) == 2:
                to_redir = '.'.join([obj[2], path[0], path[1]])

            else:
                to_redir = '.'.join(path)


        else:
            to_redir = path

        redir = redirect(url_for(to_redir, **dump))
        for k in dump:
            del self.__dict__[k]

        return redir

    def render(self, path, flask_lookup=False):
        dump = dict.copy(self.__dict__)
        path += '.html'
        if not flask_lookup:
            obj = str(self)
            obj = obj[1:obj.rfind('.')].split('.')
            
            path = path.split('/')
            if len(path) == 1:
                to_render = '/'.join([obj[2], obj[4], path[0]])

            elif len(path) == 2:
                to_render = '/'.join([obj[2], path[0], path[1]])

            else:
                to_render = '/'.join(path)

        else:
            to_render = path

        rendered = render_template(to_render, **dump)
        for k in dump:
            del self.__dict__[k]

        return rendered