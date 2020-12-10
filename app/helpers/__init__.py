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

        
        if 'namespaces' in rts:
            for namespace in rts['namespaces']:
                ns_routes = rts['namespaces'][namespace]
                for entry in ns_routes:
                    sani_route = sanitize_url(entry['route'])
                    route = f'{sani_prefix}{namespace}{sani_route}'
                    route_name = entry['name']
                    route_name = f'{prefix}.{namespace}.{route_name}'
                    action_name = entry['name']
                    if view in entry:
                        action_name = entry['view']

                    view_coll = dict_views[namespace]
                    view = getattr(view_coll, action_name)

                    methods = ['GET']
                    if 'method' in entry:
                        methods = [entry['method']]
                    
                    #print(f'Registering route {route_name} for {route} in {namespace}')
                    app.add_url_rule(route, route_name, view, methods=methods)

        