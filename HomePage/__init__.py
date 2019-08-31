import datetime
import os
import sys

from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
print(app.root_path,'*'*50)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds=1)
# app.config['DEBUG'] = True

db = SQLAlchemy(app, use_native_unicode='utf8')
bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)

from HomePage.models import MyAdminIndexView, PostAdmin, PostMessage, Blog, Message, User, UserCheck

admin = Admin(app, name='Admin', index_view=MyAdminIndexView())
admin.add_view(PostAdmin(Blog, db.session))
admin.add_view(PostMessage(Message, db.session))
admin.add_view(UserCheck(User, db.session))

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


login_manager.login_view = 'app.login'

from HomePage import views, errors, commands
