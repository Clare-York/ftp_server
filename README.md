
ftp_server:

使用pyftpdlib搭建的ftp server,修改了部分源码使其达到自定义的功能，具体改动在
handlers.py
2331~2348行

改动后，上传至根目录的文件会被自动收集至以上传日期为命名的文件夹内，而不影响上传至根目录下其他文件夹内的文件

http_server:（目前仅用于下载，因最新的Chrome和Edge等浏览器已不支持ftp://协议，固搭建了一个http的文件服务器）

使用flask搭建的文件服务器，参考了：https://www.cnblogs.com/ddzj01/p/10343325.html 的源码
该源码在windows上运行正常，在群晖NAS（linux）上会报错，我对此进行了linux环境适配，并修改了模板文件



环境  
python3.7  
Windows/linux/Mac

安装  
pip3 install -r requirements.txt

群晖下安装依赖

/var/packages/py3k/target/usr/local/bin/pip3 install -r requirements.txt

配置  
config.py

运行FTP服务  
python3 server.py

运行HTTP服务（群晖）

/var/packages/py3k/target/usr/local/bin/gunicorn -c gunicorn_config.py app:app