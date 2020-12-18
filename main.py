from app import app
import os



bp_list = os.listdir(os.path.join(os.getcwd(), 'app', 'blueprints'))
bp_list = [os.path.join(os.getcwd(), 'app', 'blueprints', bp, 'routes.yaml') for bp in bp_list]
extra_files = []
for bp in bp_list:
    if os.path.isfile(bp):
        extra_files.append(bp)

if __name__ == '__main__':
    app.run(debug=True, extra_files=extra_files)