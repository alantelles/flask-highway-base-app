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

    def edit(self, ic):
        return f'returning edit: {id}'

pocs_views = PocsViews()