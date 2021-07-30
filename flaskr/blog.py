#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/21 9:49
# @Author   : ReidChen
# Document  ：主页面功能

import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .config import DevelopmentConfig as config
from flaskr.auth import login_required
from flaskr.db_table import UserTable, PostTable
from flaskr import db
from datetime import datetime
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    # 判断当前是否已经登录，没有登录则返回登录页
    if not  g.user:
        return redirect(url_for('auth.login'))
    # 分页功能
    # page_index = request.args.get('page', 1, type=int)
    # pagination = PostTable.query.join(UserTable, PostTable.author_id == UserTable.id).order_by(
    #     PostTable.created.desc()).paginate(page_index, per_page=config.PER_POSTS_PER_PAGE,error_out=False)
    
    # posts = pagination.items
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploadDir = os.path.join(basedir, 'static/uploads')
    
    if request.method == 'GET':
        print('1111111111111111')
        f = request.files.get('selectfile')
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
    
        if f:
            filename = secure_filename(f.filename)
            types = ['jpg', 'png', 'tif']
            if filename.split('.')[-1] in types:
                uploadpath = os.path.join(uploadDir, filename)
                f.save(uploadpath)
                flash('Upload Load Successful!', 'success')
                return render_template('main/index_blank.html')
            else:
                flash('Unknown Types!', 'fail')
        else:
            flash('No File Selected.', 'fail')
    return render_template('main/index_blank.html')

    # return render_template('main/index_blank.html',
    #                        title='Index',
    #                        posts=posts,
    #                        pagination=pagination,
    #                        current_time = datetime.utcnow())
    
    
@bp.route('/upload')
def upload():
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploadDir = os.path.join(basedir, 'static/uploads')
    print('11111111111111')
    if request.method == 'POST':
        print('22222222222222222')
        f = request.files.get('selectfile')
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
        
        if f:
            filename = secure_filename(f.filename)
            types = ['jpg', 'png', 'tif']
            if filename.split('.')[-1] in types:
                uploadpath = os.path.join(uploadDir, filename)
                f.save(uploadpath)
                flash('Upload Load Successful!', 'success')
                return render_template('main/index_blank.html')
            else:
                flash('Unknown Types!', 'fail')
        else:
            flash('No File Selected.', 'fail')
    return render_template('main/index_blank.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    # 创建博客页面按钮
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            article = PostTable(title=title, body=body, author_id=g.user.id)
            db.session.add(article)

            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('main/create.html')


def get_post(id, check_author=True):
    post = PostTable.query.join(UserTable, PostTable.author_id == UserTable.id).filter(PostTable.id == id).one()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post.author_id != g.user.id:
        abort(403)
    
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # 这个id 如何拿到，如何传入
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            PostTable.query.filter(PostTable.id == id).update({'title': title, 'body': body})
            
            db.session.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('main/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    PostTable.query.filter(PostTable.id == id).delete()

    db.session.commit()
    return redirect(url_for('blog.index'))
