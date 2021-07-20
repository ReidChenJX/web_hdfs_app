#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 10:54
# @Author   : ReidChen
# Document  ：

import os
from flask import Flask

def create_app(test_config=None):
    """
    创建并配置应用
    :param test_config:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    # 如果是在测试模式下，加载测试的配置信息
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return f'Hello World !'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app