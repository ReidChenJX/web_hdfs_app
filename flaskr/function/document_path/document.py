#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/3 10:01
# @Author   : ReidChen
# Document  ：为前端页面提供当前访问路径的文件列表；提供HDFS的文件列表

import os
import time
from flaskr.config import HDFSConfig
from flaskr.function.upload_file.colle_file import LinuxToHdfs


def get_size(size):
    # 文件大小转换
    if size < 1024:
        return '%d  B' % size
    elif 1024 <= size < 1024 * 1024:
        return '%.2f KB' % (size / 1024)
    elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
        return '%.2f MB' % (size / (1024 * 1024))
    else:
        return '%.2f GB' % (size / (1024 * 1024 * 1024))


class DocumentReader:
    def __init__(self, real_path, basedir):
        self.real_path = real_path
        self.basedir = basedir
    
    def analysis_dir_local(self):
        dirs = []
        files = []
        os.chdir(self.real_path)
        
        for name in sorted(os.listdir('.'), key=lambda x: x.lower()):
            _time = time.strftime("%Y/%m/%d %H:%M", time.localtime(os.path.getctime(name)))
            if os.path.isdir(name):
                dirs.append([name,_time,'文件夹','-'])
            elif os.path.isfile(name):
                file_type = os.path.splitext(name)[-1]
                size = get_size(os.path.getsize(name))
                files.append([name, _time, file_type, size])
        os.chdir(self.basedir)
        return dirs, files
 

class HDFSReader(HDFSConfig):
    def __init__(self, real_path):
        self.real_path = real_path
        self.linux_sion = LinuxToHdfs(hosts=self.pyhdfs_hosts, user=self.hdfs_user)
        
    def analysis_dir_hdfs(self):
        '''
        拿到地址，获取该地址下 HDFS 文件路径的所有文件和文件夹
        :return:
        '''
        dirs = []
        files = []
        
        list_xattrs = self.linux_sion.list_status(self.real_path)
        print(list_xattrs)
        for f in list_xattrs:
            _time = time.strftime("%Y/%m/%d %H:%M", time.localtime(f.modificationTime // 1000))
            if f.type == 'DIRECTORY':
                dirs.append([f.pathSuffix, _time, '文件夹', '-'])
            elif f.type == 'FILE':
                file_type = f.pathSuffix.split('.')[-1]
                size = get_size(f.length)
                files.append([f.pathSuffix, _time, file_type, size])
        return dirs, files
