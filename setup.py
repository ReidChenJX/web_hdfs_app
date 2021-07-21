#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/20 10:41
# @Author   : ReidChen
# Document  ：安装文件

from setuptools import find_packages, setup

setup(
    name = 'flaskr',
    version = '1.0.0',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'flask',
    ],
)
