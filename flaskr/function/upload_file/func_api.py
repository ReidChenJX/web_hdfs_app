#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# @time     : 2021/8/4 16:11
# @Author   : ReidChen
# Document  ：对文件上传功能进行整合，提供web 需要的接口函数

from flaskr.function.upload_file.colle_file import LinuxToHdfs
from flaskr.config import HDFSConfig
import os
import shutil


HDFSConfig = HDFSConfig()
hosts = HDFSConfig.pyhdfs_hosts
user = HDFSConfig.hdfs_user
LinuxToHdfs = LinuxToHdfs(hosts, user)

def upload_web_hdfs(loacl_dir, hdfs_dir):
    LinuxToHdfs.file_to_hdfs(loacl_dir, hdfs_dir)
    # 删除linux 中间位置文件
    os.remove(loacl_dir)
    