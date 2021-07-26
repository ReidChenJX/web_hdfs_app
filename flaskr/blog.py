#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/21 9:49
# @Author   : ReidChen
# Document  ：

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db_table import UserTable, PostTable
from flaskr import db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    # 客户请求会自动创建g和app
    # db = get_db()
    posts = PostTable.query.join(UserTable, PostTable.author_id == UserTable.id).filter().order_by(
        PostTable.created.desc()).all()

    return render_template('blog/index.html', posts=posts)


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
    return render_template('blog/create.html')


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
    
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    PostTable.query.filter(PostTable.id == id).delete()

    db.session.commit()
    return redirect(url_for('blog.index'))
