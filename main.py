from app import app
import os

bp_path = os.path.join(os.getcwd(), 'app', 'blueprints', 'user_management')
rt_path = os.path.join(bp_path, 'routes.yaml')
extra_files = []
extra_files.append(rt_path)
#DON'T REMOVE: extra_files add section
#END: extra_files add section

if __name__ == '__main__':
    app.run(debug=True, extra_files=extra_files)