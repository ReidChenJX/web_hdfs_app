#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/21 9:49
# @Author   : ReidChen
# Document  ：

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
# from flaskr.db import get_db
from flaskr.db_table import UserTable,PostTable
from flaskr import db

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    # 客户请求会自动创建g和app
    # db = get_db()
    posts = PostTable.query.join(UserTable,UserTable.id==PostTable.author_id).filter().all()
    # posts = db.session.execute('SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC').fetchall()
    return render_template('blog/index.html',posts=posts)


@bp.route('/create', methods=('GET','POST'))
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
            article = PostTable(title=title,body=body,author_id=g.user['id'])
            db.session.add(article)
            # db.session.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = PostTable.query.join(UserTable,UserTable.id==PostTable.author_id).filter(id=id).one()
    # post = get_db().execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.id = ?',
    #     (id,)
    # ).fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
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
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)
    

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))















