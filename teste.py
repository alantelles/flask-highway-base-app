class UserManagementViews:
    def index(self):
        return 'me pegou'

user_management_views = UserManagementViews()

x = "index"
m = getattr(user_management_views, x)
print(m)