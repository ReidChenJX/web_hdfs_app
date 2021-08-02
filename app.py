#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/2 13:17
# @Author   : ReidChen
# Document  : 启动文件

from flaskr import create_app
import os

app = create_app()

if __name__ == '__main__':
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='172.18.0.202', port=port)
