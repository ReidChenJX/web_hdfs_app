#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 14:36
# @Author   : ReidChen
# Document  ：

import functools
import json
import datetime
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .db_table import UserTable
from .forms import LoginForm, RegisterForm, ResetPassword
from flaskr.web_design.department.dept_info import deptInfo
from flaskr.web_design.menu.menu import menuList

# 使用蓝图，蓝图的名称会添加到函数名称的前面
bp = Blueprint('auth', __name__, )

# url_prefix='/auth'
"""flask与bootstrap 后端响应"""


@bp.route('/register', methods=('GET', 'POST'))
def B_register():
    """注册"""
    if request.method == 'POST':
        # 读取连接请求中的数据
        username = request.form['username']
        password = request.form['password']
        password_f = request.form['password_f']
        error = None
        
        if not username:
            error = f'Username is required.'
        elif not password:
            error = f'Password is required.'
        elif password != password_f:
            error = f'两次密码不一致'
        elif UserTable.query.filter_by(username=username).count():
            error = f"用户名 {username} 已被注册."
        
        if error is None:
            user = UserTable(username=username,
                             password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 注册成功，返回登录页面
            return redirect(url_for('auth.B_login'))
        # 注册失败，返回错误信息
        # current_app.logger.debug(error,exc_info=
        current_app.logger.debug(error)
        flash(error)  # 储存在渲染模块时可以调用的信息
    return render_template('auth/sign-up.html', title='注册')


@bp.route('/login', methods=('GET', 'POST'))
def B_login():
    """登录"""
    # form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        # 判断登录名是否在数据库中
        user = UserTable.query.filter_by(username=username).first()
        
        if user is None:
            error = 'Incorrect username.'
        # 验证登录密码
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            # 将客户ID存储在会话的cookie中
            session['user_id'] = user.id
            session['user_name'] = user.username
            print(session)
            # 登录成功，返回首页
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('auth/login.html', title='登录')


@bp.before_app_request
def load_logged_in_user():
    # 在登录前查看是否已经存储早cookie中
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = UserTable.query.filter_by(id=user_id).first_or_404()


@bp.route('/logout')
def B_logout():
    # 注销当前账户
    session.clear()
    return redirect(url_for('auth.B_login'))


def login_required(view):
    # 判断用户是否载入，若未载入则跳转登录页面
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.B_login'))

        return view(**kwargs)
    return wrapped_view


"""flask与VUE后端响应"""


@bp.route('/system/login', methods=('GET', 'POST'))
def V_login():
    """登录
    :return: resp
    """
    if request.method == 'POST':
        # vue 前端返回JSON格式，需解码
        post_data = json.loads(request.get_data())
        username = post_data['stUserName']
        password = post_data['stPassword']
        print(password)
        # 判断登录名是否在数据库中
        user = UserTable.query.filter_by(username=username).first()
        # 需返回数据
        msg, stName, dept_Info, roleList, menu_List, token, code = None, None, None, None, None, None, None
        
        if user is None:
            code = 1
            msg = '用户不存在.'
        elif not check_password_hash(user.password, password):
            # 验证登录密码
            code = 2
            msg = '用户名密码错误.'
        
        if msg is None:
            # 登录成功，返回数据
            code = 0
            msg = '操作成功'
            token = str(user.id) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%I:%M:%S")
            stName = user.username
            dept_Info = deptInfo
            roleList = [1, 2]
            menu_List = menuList
            
            # 登录成功，在session中保存信息
            session['user_name'] = stName
            session['user_id'] = user.id
        
        userInfo = {'stName': stName}
        user = {'userInfo': userInfo, 'deptInfo': dept_Info, 'roleList': roleList, 'menuList': menu_List}
        data = {'token': token, 'user': user}
        resp = {'msg': msg, 'code': code, 'data': data}
        return (jsonify(resp))


@bp.route('/system/logout')
def V_logout():
    # 注销当前账户
    post_data = json.loads(request.get_data())
    username = post_data['stUserName']
    session.pop('user_name', username)
    return
