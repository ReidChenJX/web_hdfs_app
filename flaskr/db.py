#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 13:54
# @Author   : ReidChen
# Document  ：

import sqlite3
from flask_sqlalchemy import SQLAlchemy
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    # 通过g 生成连接会话，并确定会话中的数据库连接
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
        g.db = SQLAlchemy(current_app)
        
    return g.db

def close_db(e=None):
    # 关闭数据连接
    db = g.pop('db',None)
    
    if db is not None:
        db.close()

def init_db():
    # 初始化数据库
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.session.execute(f.read().decode('utf8'))
        
@click.command('init_db')
@with_appcontext
def init_db_command():
    # 以命令行的形式初始化数据库，并输出完成语句
    init_db()
    click.echo('Initialized the database.')
    

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)




