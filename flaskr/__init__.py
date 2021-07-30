#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 10:54
# @Author   : ReidChen
# Document  ：

import os
import json
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from .config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

def create_app(test_config=None):
    """
    创建并配置应用
    :param test_config:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Database set
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploadDir = os.path.join(basedir, 'static/database')
    with open(uploadDir, 'r') as load_f:
        data_info = json.load(load_f)
    
    database_url = 'postgresql+psycopg2://{user}:{passwd}@{ip}:{port}/{database}'.format(
        user=data_info['user'], passwd=data_info['passwd'], ip=data_info['ip'],
        port=data_info['port'], database=data_info['database']
    )
    
    # 配置管理
    if test_config is None:
        app.config.from_object(config['default'])
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # 如果是在测试模式下，加载测试的配置信息
        app.config.from_object(config['testing'])
    
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return f'Hello World !'

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    
    # from . import auth, upload
    from . import auth,blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    # app.register_blueprint(upload.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
