#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 13:54
# @Author   : ReidChen
# Document  ：

import sqlite3
from flask_sqlalchemy import SQLAlchemy
import click
from datetime import datetime

from flask import current_app, g
from flask.cli import with_appcontext
from . import db


def init_db():
    # 初始化数据库
    with current_app.open_resource('schema.sql') as f:
        db.session.execute(f.read().decode('utf8'))


@click.command('init_db')
@with_appcontext
def init_db_command():
    # 以命令行的形式初始化数据库，并输出完成语句
    init_db()
    click.echo('Initialized the database.')


# 维护系统使用的所有表单，作为ORM的目标

class UserTable(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128))




class PostTable(db.Model):
    __tablename__ = 'post_table'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
