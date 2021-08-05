#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/19 10:35
# @Author   : ReidChen
# Document  ：Download the file from the hdfs

import hdfs
import pyhdfs
import os
import time

class HdfsToLocal:
    def __init__(self, hosts):
        # 采用 hdfs 的链接获取文件
        self.hosts = hosts      # 分号间隔
        self.client = hdfs.client.InsecureClient(self.hosts)
        
    
    def down_file(self, file, local_path, threads=3, overwrite=True):
        """ 将hdfs 文件下载到本地
        :param file: hdfs 文件地址，可以是具体文件，也可以是目录地址
        :param local_path: 下载到本地地址
        :param threads: 并行数量，若为文件则并行为0
        """
        self.client.download(hdfs_path=file,local_path=local_path,overwrite=overwrite,
                             n_threads=threads)
    
    def delete(self, file, recursive=False):
        """删除文件
        :param file: 文件或文件目录
        :param recursive: 递归删除，如果需要删除非空目录，则设置为True
        """
        self.client.delete(hdfs_path=file, recursive=recursive)
        
        
    def content(self, hdfs_path):
        """返回文件或目录 详情
        :param hdfs_path:
        """
        return self.client.content(hdfs_path=hdfs_path)
    
    def list(self, hdfs_path):
        """返回文件目录
        :param hdfs_path:
        """
        return self.client.list(hdfs_path)



        