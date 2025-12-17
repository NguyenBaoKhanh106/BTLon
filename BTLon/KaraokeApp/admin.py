from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from KaraokeApp import app, db
from KaraokeApp.models import Room, User, Branch, UserRoleEnum
from flask_login import current_user, logout_user
from flask import redirect

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('/admin/index.html')


class MyUserView(ModelView):
    column_list = ['name', 'username', 'role', 'active']
    column_searchable_list = ['name', 'username']
    column_filters = ['role']

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN

    def is_visible(self):
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN

class MyModelView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN

    def is_visible(self):
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN


class MyAdminLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect('/admin')

    def is_visible(self):
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN


admin = Admin(app=app, name="TLKaraoke", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyModelView(Room, db.session))
admin.add_view(MyModelView(Branch, db.session))
admin.add_view(MyAdminLogoutView("Đăng xuất"))