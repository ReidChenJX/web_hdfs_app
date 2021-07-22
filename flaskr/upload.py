#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/22 11:34
# @Author   : ReidChen
# Document  ：

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
import os

bp = Blueprint('blog',__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
uploadDir = os.path.join(basedir,'static/uploads')

@bp.route('/upload', methods=('GET','POST'))
def upload():
    if request.method=='POST':
        f = request.files.get('selectfile')
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
            