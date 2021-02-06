# -*- coding: utf-8 -*-
"""
@Time        : 2021/2/6 9:03
@Author      : chengy_work@foxmail.com
@File        : http_server.py
@Introduce   : http服务文件
"""
import os
import time
import math
from flask import Flask, render_template, url_for, redirect, send_from_directory
from config import *
from urllib import parse
import platform

app = Flask(__name__)
system = platform.system()


@app.route("/")
def index():
    """
    入口，自动跳转至网盘页
    :return:
    """
    return redirect(url_for("docs"))


@app.route('/doc/')
@app.route('/doc/<path:subdir>/')
def docs(subdir=''):
    """
    列出指定目录下所有内容
    :param subdir: 传入的路径
    :return:
    """
    subdir = parse.unquote(subdir)  # 汉字的url编码解析回汉字
    flag, backup = cwd(subdir)
    if not flag:
        return redirect(url_for('downloader', fullname=backup))
    contents = make_response_data(subdir)
    return render_template('index.html', contents=contents, backup=backup, subdir=subdir,
                           ossep=os.sep)


@app.route('/download/<path:fullname>')
def downloader(fullname):
    """
    下载文件
    :param fullname: 传入的文件路径
    :return:
    """
    fullname = parse.unquote(fullname)
    if system == "Windows":
        filename = fullname.split("\\")[-1]
        dir_path = fullname[:-len(filename)]
    else:
        filename = fullname.split("/")[-1]
        dir_path = os.path.join("/", fullname[:-len(filename)])
    return send_from_directory(dir_path, filename, as_attachment=True)


def cwd(subdir):
    """
    切换工作目录
    :param subdir: 动态路由路径
    :return:
    """
    if subdir == '':
        # 名字为空，切换到根目录
        os.chdir(homedir)
        backup = ""
    else:
        if system == "Windows":
            if "\\" in subdir:
                name = subdir.split("\\")[-2]
                backup = os.path.join(subdir.split(name)[0], name)
            else:
                backup = ""
        else:
            name = subdir.split("/")[-1]
            backup = subdir.split(name)[0]  # 获取上级目录
        fullname = homedir + os.sep + subdir
        #  如果是文件，则下载
        if not os.path.isdir(fullname):
            return 0, fullname
        #  如果是目录，切换到该目录下面
        else:
            os.chdir(fullname)
    return 1, backup


def make_response_data(subdir):
    """
    生成渲染模板所需要的的数据
    :return:
    """
    current_dir = os.getcwd()  # 获取当前目录
    current_list = os.listdir(current_dir)  # 目录转列表
    contents = []
    for item in sorted(current_list):
        content = {}
        fullpath = current_dir + os.sep + item
        # 如果是目录，在后面添加一个sep
        if os.path.isdir(fullpath):
            extra = os.sep
            content['size'] = ""
            content['type'] = "dir"  # tpye用于给模板设置图标
        else:
            extra = ''
            content['size'] = strftime_size(os.path.getsize(fullpath))
            content['type'] = "file"
        content['filename'] = item + extra
        content['url'] = os.path.join(subdir, item)
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        contents.append(content)
    return contents


def strftime_size(size):
    """
    os获取的文件大小是以 B（字节）为单位，该方法将字节转换为其他单位输出
    :param size: 文件大小
    :return:
    """
    if size < 1024 ** 2:
        new = math.ceil(size / 1024)
        return "{} KB".format(new)
    elif 1024 ** 2 <= size < 1024 ** 3:
        num = 1024 ** 2
        new = round(size / num, 2)
        return "{} MB".format(new)
    elif 1024 ** 3 <= size < 1024 ** 4:
        num = 1024 ** 3
        new = round(size / num, 2)
        return "{} GB".format(new)
    else:
        num = 1024 ** 4
        new = round(size / num, 2)
        return "{} TB".format(new)


if __name__ == '__main__':
    app.run(*http_address, debug=debug)
