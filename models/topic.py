import time
from models import Model


class Topic(Model):
    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id', '')
        self.board_id = int(form.get('board_id', -1))

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def time(self):
        time_format = '%Y/%m/%d %H:%M:%S'
        localtime = time.localtime(self.ct)
        formatted = time.strftime(time_format, localtime)
        return formatted

    def user(self):
        from .user import User
        user = User.find_by(id=self.user_id)
        return user.username

    def days(self):
        now = int(time.time())
        t_ia = now-self.ct
        day = t_ia // 86400
        if day == 0:
            return '今天'
        else:
            return '{}天前'.format(day)

    def borad(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def board_title(self):
        from .board import Board
        if self.board_id == -1:
            return '未分类'
        else:
            b = Board.find(self.board_id)
            return b.title

    def user_image(self):
        from .user import User
        u = User.find(self.user_id)
        return u.user_image


