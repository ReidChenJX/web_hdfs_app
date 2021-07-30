#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/22 11:34
# @Author   : ReidChen
# Document  ：

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
# from flaskr.db import get_db
import os

bp = Blueprint('upload', __name__)

basedir = os.path.abspath(os.path.dirname(__file__))
uploadDir = os.path.join(basedir, 'static/uploads')


@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
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
                return render_template('upload/upload.html', imagename=filename)
            else:
                flash('Unknown Types!', 'danger')
        else:
            flash('No File Selected.', 'danger')
    return render_template('upload/upload.html')
