#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 10:54
# @Author   : ReidChen
# Document  ：

import os
import json
import logging
import time
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from .config import config
from .BaseError import BaseError, ValidationError, NotFoundError, FormError, OrmError

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
    databaseDir = os.path.join(basedir, 'static/database')
    with open(databaseDir, 'r') as load_f:
        data_info = json.load(load_f)
    
    database_url = 'postgresql+psycopg2://{user}:{passwd}@{ip}:{port}/{database}'.format(
        user=data_info['user'], passwd=data_info['passwd'], ip=data_info['ip'],
        port=data_info['port'], database=data_info['database']
    )
    
    # 配置管理
    if test_config is None:
        app.config.from_object(config['default'])
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['basedir'] = os.path.abspath(os.path.dirname(__file__))
        app.config['hdfs_dir'] = '/filehouse/'
    else:
        # 如果是在测试模式下，加载测试的配置信息
        app.config.from_object(config['testing'])
    
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    
    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    
    # 蓝图
    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    # app.register_blueprint(upload.bp)
    app.add_url_rule('/', endpoint='index')
    
    @app.template_filter("split_path")
    def split_path(path):
        path_list = path.split('/')
        path_list = [[path_list[i - 1], '/'.join(path_list[:i])] for i in range(1, len(path_list) + 1)]
        return path_list

    # 日志功能-按时间创建日志文件
    log_file_name = 'log/logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_dir = os.path.join(basedir,log_file_name)
    if not os.path.exists(log_file_dir):
        open(log_file_dir, 'w').close()
    
    handler = logging.FileHandler(log_file_dir, encoding='UTF-8')
    # 控制日志写入级别：基础级别：DEBUG
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)

    app.logger.addHandler(handler)

    return app
