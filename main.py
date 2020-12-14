from app import app
import os

bp_path = os.path.join('app', 'blueprints', 'user_management')
extra_files = []
print(os.path.join(bp_path, 'routes.yaml'))
extra_files.append(os.path.join(bp_path, 'user_management', 'routes.yaml'))

if __name__ == '__main__':
    app.run(debug=True, extra_files=extra_files)