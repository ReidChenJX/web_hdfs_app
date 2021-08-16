#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/26 11:45
# @Author   : ReidChen
# Document  ：

from flaskr import db
import functools
import json
import time
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db_table import UserTable

user = UserTable.query.filter_by(username=username).first()