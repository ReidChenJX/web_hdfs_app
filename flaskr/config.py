#!/usr/bin/python3
# -*- coding:UTF-8 -*-
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

class HDFSConfig:
    # 维护 HDFS 地址与对应的数据库地址
    # Linux环境
    linux_ip = '172.18.0.202'
    linux_user = 'root'
    linux_passwd = 'sangfor@2021'
    # HDFS 环境
    pyhdfs_hosts = '172.18.0.202:50070,172.18.0.203:50070'
    hdfs_user = 'hadoop'
    # 地址信息
    linux_path = '/home/project/tmp_file/'
    hdfs_path = '/filehouse/'       # HDFS 对于文件管理系统的跟目录

    # 中间数据库地址
    # 向中间库写入地址对应关系
    ip = '172.18.0.201'
    port = '5432'
    user = 'postgres'
    passwd = 'wavenet'
    database = 'flask_app'