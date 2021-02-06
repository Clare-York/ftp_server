# -*- coding: utf-8 -*-
"""
@Time        : 2021/1/27 11:06
@Author      : chengy_work@foxmail.com
@File        : ftp_server.py
@Introduce   : FTP服务器
"""
from pyftpdlib.authorizers import DummyAuthorizer
from handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import LogFormatter
import logging
import os
from config import *
from logging import handlers
from datetime import datetime


class FTP(object):
    """
    FTP server
    """

    def __init__(self):
        if not os.path.exists(homedir):
            os.mkdir(homedir)
        self.authorizer = DummyAuthorizer()  # 实例化虚拟用户，这是FTP验证首要条件
        self.handler = FTPHandler  # 初始化ftp句柄
        self.dtp_handler = ThrottledDTPHandler  # 初始化传输句柄
        self.set_log_config()
        self.set_user_config()
        self.set_handler_config()
        self.set_other_config()

    def set_user_config(self):
        """
        配置FTP user
        :return:
        """
        # 添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限),可以为不同的用户添加不同的目录和权限
        self.authorizer.add_user(username, password, homedir, perm="elradfmw")
        # 添加匿名用户 只需要路径
        self.authorizer.add_anonymous(homedir)

    def set_handler_config(self):
        """
        配置FTP handler
        """
        self.handler.authorizer = self.authorizer
        self.handler.passive_ports = range(*passive)  # 添加被动端口范围

    def set_other_config(self):
        """
        其他配置
        :return:
        """
        if not os.listdir(homedir):
            # 如果根目录是空就创建一个目录进去
            dirname = datetime.now().strftime('%Y-%m-%d')
            dirpath = os.path.join(homedir, dirname)
            os.mkdir(dirpath)
        # 下载上传速度设置
        self.dtp_handler.read_limit = 1024 ** 5  # 1000Mb/s
        self.dtp_handler.write_limit = 1024 ** 5  # 1000Mb/s

    def run(self):
        """
        启动服务
        :return:
        """

        # 监听ip 和 端口,linux里需要root用户才能使用21端口
        server = FTPServer(ftp_address, self.handler)
        # 最大连接数
        server.max_cons = 150
        server.max_cons_per_ip = 15
        # 开始服务，自带日志打印信息
        server.serve_forever()

    @staticmethod
    def set_log_config():
        """
        配置日志
        :return:
        """
        # 配置日志存储位置
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        # 日志名称绝对路径
        log_file = os.path.join(log_dir, log_name)
        # 记录日志，默认情况下日志仅输出到屏幕（终端）
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        fh = handlers.TimedRotatingFileHandler(log_file, when='D', backupCount=30)
        fh.suffix = "%Y-%m-%d.log"
        ch.setFormatter(LogFormatter())
        fh.setFormatter(LogFormatter())
        logger.addHandler(ch)  # 将日志输出至屏幕
        logger.addHandler(fh)  # 将日志输出至文件


if __name__ == '__main__':
    ftp_server = FTP()
    ftp_server.run()
