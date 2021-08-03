#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/3 10:01
# @Author   : ReidChen
# Document  ：为前端页面提供当前访问路径的文件列表；提供HDFS的文件列表

import os
import time


class DocumentReader:
    def __init__(self, real_path):
        self.real_path = real_path
    
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
                size = self.get_size(os.path.getsize(name))
                files.append([name, _time, file_type, size])
        return dirs, files
                
                
    @staticmethod
    def get_size(size):
        if size < 1024:
            return '%d  B' % size
        elif 1024 <= size < 1024 * 1024:
            return '%.2f KB' % (size / 1024)
        elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
            return '%.2f MB' % (size / (1024 * 1024))
        else:
            return '%.2f GB' % (size / (1024 * 1024 * 1024))