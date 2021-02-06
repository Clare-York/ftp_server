# -*- coding: utf-8 -*-
"""
@Time        : 2021/1/27 13:27
@Author      : chengy_work@foxmail.com
@File        : config.py
@Introduce   : 配置文件
"""
# 调试
debug = True

# 日志名称
log_name = "ftp-server.log"

# FTP用户名
username = "user"

# FTP用户密码
password = "123456"

# FTP用户根目录
homedir = r"/volume2/Download/FTP_files"  # 群晖配置
# homedir = r"/home/files"  # linux配置
# homedir = r"D:\www"  # Windows配置

# FTP服务监听地址
ftp_address = ("0.0.0.0", 21)

# 被动端口范围
passive = [3000, 4000]

# HTTP服务监听地址（开发环境）
http_address = ("0.0.0.0", 8000)
