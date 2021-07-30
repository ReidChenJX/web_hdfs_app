#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/26 10:23
# @Author   : ReidChen
# Document  ：配置文件

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # 显示分页
    PER_POSTS_PER_PAGE = 8



class DevelopmentConfig(Config):
    """一般环境"""
    DEBUG = True
    ''' 邮件系统
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_POST = 25
    MAIL_USERNAME = '@foxmail.com'
    MAIL_PASSWORD = ' '
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    '''
    ENABLE_THREADS = True
    # SQLALCHEMY_DATABASE_URI 在 init 中读取文件地址后传入
    
class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI 在 测试环境下的数据库地址
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}