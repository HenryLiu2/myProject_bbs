import time
from flask import jsonify
from models import Model


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.topic_id = int(form.get('topic_id', -1))

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def days(self):
        now = int(time.time())
        t_ia = now-self.ct
        day = t_ia // 86400
        if day == 0:
            return '今天'
        else:
            return '{}天前'.format(day)
