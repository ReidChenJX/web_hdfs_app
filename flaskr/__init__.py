#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 10:54
# @Author   : ReidChen
# Document  ：

import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

