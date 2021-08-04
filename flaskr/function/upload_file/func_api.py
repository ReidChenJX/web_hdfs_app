#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/4 16:11
# @Author   : ReidChen
# Document  ：对文件上传功能进行整合，提供web 需要的接口函数

from flaskr.function.upload_file.colle_file import LinuxToHdfs
from flaskr.config import HDFSConfig


HDFSConfig = HDFSConfig()
hosts = HDFSConfig.pyhdfs_hosts
user = HDFSConfig.user
LinuxToHdfs = LinuxToHdfs(hosts, user)

def upload_web_hdfs():



    pass