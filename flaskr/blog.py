#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/21 9:49
# @Author   : ReidChen
# Document  ：主页面功能

import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, current_app, \
    send_from_directory
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db_table import UserTable, PostTable
from flaskr import db
from flaskr.function.document_path.document import DocumentReader, HDFSReader
from flaskr.function.upload_file.colle_file import LinuxToHdfs

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # 分页功能
    # page_index = request.args.get('page', 1, type=int)
    # pagination = PostTable.query.join(UserTable, PostTable.author_id == UserTable.id).order_by(
    #     PostTable.created.desc()).paginate(page_index, per_page=config.PER_POSTS_PER_PAGE,error_out=False)
    
    # posts = pagination.items
    
    if request.method == 'POST':
        print('Succeed')
    
    return render_template('main/index_blank.html')


@bp.route('/dir', methods=['GET', 'POST'])
@bp.route('/dir/<path:path_uri>', methods=['GET', 'POST'])
def dir_local(path_uri=''):
    base_dir = current_app.config['basedir']
    real_path = os.path.join(base_dir, path_uri)
    if not os.path.exists(real_path):
        return render_template('main/dir_local.html', error_info='错误的路径...')
    file_reader = DocumentReader(real_path, base_dir)
    dirs, files = file_reader.analysis_dir_local()
    
    return render_template('main/dir_local.html', path=path_uri, dirs=dirs, files=files, error_info=None)


@bp.route('/hdfs', methods=['GET', 'POST'])
@bp.route('/hdfs/<path:path_uri>', methods=['GET', 'POST'])
def dir_hdfs(path_uri=''):
    # 主页面，文件路径,与index区分开
    
    hdfs_dir = current_app.config['hdfs_dir']
    real_path = os.path.join(hdfs_dir, path_uri)
    
    file_reader = HDFSReader(real_path)
    
    if not file_reader.linux_sion.exists(real_path):
        return render_template('main/dir_local.html', error_info="错误的路径...")
    dirs, files = file_reader.analysis_dir_hdfs()
    
    return render_template('main/dir_hdfs.html', path=path_uri, dirs=dirs, files=files, error_info=None)


def split_path(path):
    path_list = path.split('/')
    path_list = [[path_list[i - 1], '/'.join(path_list[:i])] for i in range(1, len(path_list) + 1)]
    return path_list


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    # 文件上传功能,异步上传，只用考虑单文件情况
    basedir = os.path.abspath(os.path.dirname(__file__))
    session_name = session['user_name']
    uploadDir = os.path.join(basedir, 'FileRecv/{username}'.format(username=session_name))
    
    if request.method == 'GET':
        return "is upload file ... "
    else:
        f = request.files.get('md5file')
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
        
        filename = f.filename
        uploadpath = os.path.join(uploadDir, filename)
        f.save(uploadpath)
        # 本地文件上传至服务器后，将服务器文件上传至HDFS
        local_file_path = ''
        hdfs_file_path = ''
        # funcation
        return jsonify({"code": 200,
                        "info": "文件：%s 上传成功" % filename})


@bp.route('/download/<filename>')
@bp.route('/download/<path:path>/<filename>')
def download(filename, path=None):
    # 页面下载文件功能
    if not path:
        real_path = current_app.config['basedir']
    else:
        real_path = os.path.join(current_app.config['basedir'], path)
    return send_from_directory(real_path, filename, mimetype='application/octet-stream')


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
