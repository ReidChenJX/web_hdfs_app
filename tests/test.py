#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/26 11:45
# @Author   : ReidChen
# Document  ：

from flaskr import db
from flaskr.db_table import UserTable

a = UserTable.query.filter_by(username='cjx')