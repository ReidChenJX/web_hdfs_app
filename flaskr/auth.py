#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 14:36
# @Author   : ReidChen
# Document  ：

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# 使用蓝图，蓝图的名称会添加到函数名称的前面
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """注册"""
    if request.method == 'POST':
        # 读取连接请求中的数据
        username = request.form['username']
        password = request.form['password']
        db = get_db()       # 创建数据库会话
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('select id from user where username = ?',(username,)).fetchone() is not None:
            error = f"User {username} is already registered."
        if error is None:
            # 存储账户密码,密码加密
            db.execute('insert into user (username,password) values (?,?)',
                       (username, generate_password_hash(password)))
            db.commit()
            # 注册成功，返回登录页面
            return redirect(url_for('auth.login'))
        # 注册失败，返回错误信息
        flash(error)        # 储存在渲染模块时可以调用的信息
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """登录"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()  # 创建数据库会话
        error = None
        # 判断登录名是否在数据库中
        user = db.execute('select * from user where username = ?',(username)).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        # 验证登录密码
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'
            
        if error in None:
            session.clear()
            # 将客户ID存储在会话的cookie中
            session['user_id'] = user['id']
            # 登录成功，返回首页
            return redirect(url_for('index'))
            
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    # 在登录前查看是否已经存储早cookie中
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?',(user_id,)).fetchone()
        
@bp.route('/logout')
def logout():
    # 注销当前账户
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # 判断用户是否载入，若未载入则跳转登录页面
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view



