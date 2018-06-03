""""

"""
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *
from models.board import Board
from models.topic import Topic
from models.reply import Reply
import uuid

main = Blueprint('topic', __name__)

# set 具有O(1)的复杂度
csrf_tokens = set()


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    # u = current_user()
    # csrf_tokens['token'] = u.id
    return render_template("topic/index.html", ms=ms, token=token, bs=bs)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    t = Topic.find(id)
    # 判断token是否是我们给的
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        if u is not None and t.user_id == u.id:
            Topic.delete(id)
            rs = Reply.find_all(topic_id=id)
            for r in rs:
                Reply.delete(r.id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)

