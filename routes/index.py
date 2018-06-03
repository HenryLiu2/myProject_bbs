from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)

from models.user import User
from werkzeug.utils import secure_filename
from config import user_file_director
import os
from utils import log

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


# 做后缀过滤
def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/add_img', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # 做一下处理 一个用户只能上传一个头像
    # 提取出id 如果存在就先删除原先的 然后在保存现在的
    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_file_director)
        Done = False
        for file_name in os.listdir(file_path):
                i = 0
                for s in file_name:
                    if s == '_' and i != 4:
                        break
                    else:
                        i += 1
                number_str = file_name[8:i]
                # log('图片名：', file_name)
                # log('_位置：', i)
                if number_str == str(u.id):
                    new_path = os.path.join(user_file_director, file_name)
                    os.remove(new_path)
                    id_str = 'user_id='+str(u.id)+r'_'+filename
                    path = os.path.join(user_file_director, id_str)
                    # log('合成路径：', path)
                    file.save(path)
                    u.user_image = id_str
                    u.save()
                    Done = True
                    break
        if Done is False:
                    id_str = 'user_id='+str(u.id)+r'_'+filename
                    path = os.path.join(user_file_director, id_str)
                    # log('合成路径：', path)
                    file.save(path)
                    u.user_image = id_str
                    u.save()

    return redirect(url_for(".profile"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    log('文件名：', filename)
    return send_from_directory(user_file_director, filename)

