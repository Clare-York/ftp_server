# -*- coding: utf-8 -*-
"""
@Time        : 2021/2/6 13:16
@Author      : chengy_work@foxmail.com
@File        : gunicorn_config.py
@Introduce   : gunicorn的配置文件，用于在生产环境部署时引用
"""
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

# debug = True

bind = "0.0.0.0:8000"

pidfile = "logs/gunicorn.pid"

loglevel = 'debug'

accesslog = "logs/access.log"

errorlog = "logs/debug.log"

daemon = True  # 守护模式运行（后台运行）

# 启动的进程数
workers = multiprocessing.cpu_count()  # 根据CPU核心数自动选择

worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
