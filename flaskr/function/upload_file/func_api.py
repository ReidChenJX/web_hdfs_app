#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# @time     : 2021/8/4 16:11
# @Author   : ReidChen
# Document  ：对文件上传功能进行整合，提供web 需要的接口函数

from flaskr.function.upload_file.colle_file import LinuxToHdfs
from flaskr.function.upload_file.down_file import HdfsToLocal
from flaskr.config import HDFSConfig
import os
import shutil

HDFSConfig = HDFSConfig()
# 上传文件配置
hosts = HDFSConfig.pyhdfs_hosts
user = HDFSConfig.hdfs_user
LinuxToHdfs = LinuxToHdfs(hosts, user)
# 下载文件配置
hdfs_host = HDFSConfig.hdfs_host
HdfsToLinux = HdfsToLocal(hdfs_host)

def upload_web_hdfs(loacl_dir, hdfs_dir):
    # 上传web文件
    LinuxToHdfs.file_to_hdfs(loacl_dir, hdfs_dir)
    # 删除linux 中间位置文件
    os.remove(loacl_dir)
    

def down_hdfs_web(hdfs_dir, loacl_dir):
    # 下载 HDFS文件到本地
    # hdfs_dir 支持具体文件与目录，这里为具体文件地址
    HdfsToLinux.down_file(file=hdfs_dir, local_path=loacl_dir)
    