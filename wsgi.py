#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app

sys.path.insert(0, abspath(dirname(__file__)))

application = app.app

"""
建立一个gunicorn软连接
ln -s /root/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf


建立一个nginx软连接
ln -s /root/bbs/bbs.nginx  /etc/nginx/sites-enabled/bbs.nginx
 
~ cat /etc/supervisor/conf.d/bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/root/bbs
autostart=true
autorestart=true

"""
