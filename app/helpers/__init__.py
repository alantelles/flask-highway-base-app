import yaml, os
from app import app

def sanitize_url(prefix, place='both'):
    if place in ['both', 'left']:
        if prefix.find('/') != 0:
            prefix = f'/{prefix}'
    if place in ['both', 'right']:
        if prefix.rfind('/') != len(prefix) - 1:
            prefix = f'{prefix}/'
    return prefix

def register_routes(blueprint_name, **views_collections):
    dict_views = locals()['views_collections']
    #(f'{URL_PREFIX}/users/', 'user_management.users.index', users_views.index, methods=['GET'])
    
    bp_path = os.path.join(os.getcwd(), 'app', 'blueprints', blueprint_name)
    with open(f'{bp_path}/routes.yaml') as routes:
        rts = yaml.load(routes, Loader=yaml.FullLoader)
        log_register = False
        if 'log_register' in rts:
            log_register = True
        prefix = blueprint_name
        if 'url_prefix' in rts:
            prefix = rts['url_prefix']
        sani_prefix = sanitize_url(prefix)
        if 'root' in rts:
            root = rts['root']
            vc_name = root[:root.find('.')]
            action_name = root[root.find('.') + 1:]
            view_coll = dict_views[vc_name]
            view = getattr(view_coll, action_name)
            app.add_url_rule(sani_prefix, root, view, methods=['GET'])

        else:
            print("You are not registering a root route for this blueprint. It's likely an error")

        VIEWS_KEYS_NAME = 'views'
        if VIEWS_KEYS_NAME in rts:
            for namespace in rts[VIEWS_KEYS_NAME]:
                
                ns_data = rts[VIEWS_KEYS_NAME][namespace]

                # prefix get
                
                full_prefix = f'{sani_prefix}{namespace}'
                if 'url_prefix' in ns_data:
                    full_prefix = sanitize_url(ns_data['url_prefix']).format(blueprint=blueprint_name, views=namespace)

                # routes register
                if 'routes' in ns_data:
                    ns_routes = ns_data['routes']
                    
                    for entry in ns_routes:
                        sani_route = sanitize_url(entry['route'])
                        route = f'{full_prefix}{sani_route}'
                        route_name = entry['name']
                        route_name = f'{blueprint_name}.{namespace}.{route_name}'
                        action_name = entry['name']
                        if view in entry:
                            action_name = entry['view']

                        view_coll = dict_views[namespace]
                        view = getattr(view_coll, action_name)

                        methods = ['GET']
                        if 'method' in entry:
                            methods = [entry['method']]
                        if log_register:
                            print(f'Registering route {route_name} for {route} in {namespace} with methods {methods}')
                        app.add_url_rule(route, route_name, view, methods=methods)

                # resources register
                if 'resources' in ns_data:
                    res_routes = {
                        'index': '',
                        'new': 'new',
                        'create': '',
                        'show': '<int:id>',
                        'edit': '<int:id>/edit',
                        'update': '<int:id>',
                        'destroy': '<int:id>'
                    }
                    resources = ['index', 'show', 'new', 'edit', 'create', 'update', 'destroy']
                    ns_res = ns_data['resources']
                    no_resources_mod = len(ns_res.keys()) == 0
                    if not no_resources_mod:
                        will_create = []
                        
                        if 'only' in ns_res:
                            for opt in ns_res['only']:
                                if opt in resources:
                                    will_create.append(opt)

                        else:
                            will_create = resources

                        if 'except' in ns_res:
                            for opt in ns_res['except']:
                                if opt in will_create:
                                    will_create.remove(opt)

                    else:
                        will_create = resources

                    for res in will_create:
                        
                        route_name = res
                        route_name = f'{blueprint_name}.{namespace}.{res}'
                        action_name = res
                        view_coll = dict_views[namespace]
                        view = getattr(view_coll, action_name)
                        
                        if res in ['index', 'new', 'show', 'edit']:
                            methods = ['GET']

                        elif res == 'create':
                            methods = ['POST']

                        elif res == 'update':
                            methods = ['PUT', 'PATCH', 'POST']

                        elif res == 'destroy':
                            methods = ['DELETE']

                        sani_route = sanitize_url(res_routes[res])
                        route = f'{full_prefix}{sani_route}'

                        if log_register:
                            print(f'Registering route {route_name} for {route} in {namespace} with methods {methods}')

                        app.add_url_rule(route, route_name, view, methods=methods)