#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/21 14:45
# @Author   : ReidChen
# Document  ：

from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'