from app import app, db, dao
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.Models import Thuoc, DonViThuoc, UserRoleEnum
from flask_login import current_user, logout_user, login_user
from flask import redirect, request
from flask_admin import Admin, expose, AdminIndexView
from app import utils


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        return self.render('admin/admin.html',
                           tanSuat=dao.tan_suat_su_dung_thuoc(month=month),
                           money=dao.money_stats(month=month))


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.Admin)


class DrugFrequency(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')

        return self.render('admin/DrugFrequency.html',
                           tanSuat=dao.tan_suat_su_dung_thuoc(month=month))

    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.Admin)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class MyRevenueView(BaseView):
    @expose('/')
    def index(self):
        # mon_choice = request.form.get('month')
        # if mon_choice:
        return self.render('admin/stats.html', stats=dao.revenue_mon_stats(2024))

    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.Admin)


class MyRevenueMonView(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        # if mon_choice:
        return self.render('admin/statsremonth.html',
                           mon_stats=dao.receipt_detail_info(2024, month))

    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.Admin)


class ExaminationFrequency(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        # if mon_choice:
        return self.render('admin/thongkestats.html',
                           tanSuat=dao.tan_suat_kham(month))

    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.Admin)


admin = Admin(app=app, name='THỐNG KÊ BÁO CÁO', template_mode='bootstrap4', index_view=MyAdmin())
admin.add_view(MyRevenueView(name='Doanh thu tong quat'))
admin.add_view(MyRevenueMonView(name='Doanh thu'))
admin.add_view(DrugFrequency(name='Thống kê tần suất sử dụng thuốc'))
admin.add_view(ExaminationFrequency(name='Thống kê tần suất khám'))
admin.add_view(LogoutView(name='Logout'))
