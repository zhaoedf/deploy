import datetime

from flask_ckeditor import CKEditorField
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask import url_for,redirect
from flask_login import current_user
from flask_admin import AdminIndexView
from werkzeug.security import generate_password_hash, check_password_hash


from HomePage import db


# Customized Post model admin
class PostAdmin(ModelView):
    # override form type with CKEditorField
    form_overrides = dict(text=CKEditorField)
    create_template = 'blogEdit.html'
    edit_template = 'blogEdit.html'

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class PostMessage(ModelView):
    form_overrides = dict(text=CKEditorField)
    create_template = 'blogEdit.html'
    edit_template = 'blogEdit.html'

class UserCheck(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))



class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    mail = db.Column(db.String(40))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)
    type = db.Column(db.String(15))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

