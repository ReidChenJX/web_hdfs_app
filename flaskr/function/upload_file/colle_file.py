#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# @time     : 2021/7/8 11:19
# @Author   : ReidChen
# Document  ：Collect files and move it to Hdfs. 改用PSCP执行命令
# PSCP 在安装后第一次需要手动在CMD命令对目标Linux进行通信，以存储Cache

import pyhdfs
import winrm
import os
import socket


class LinuxToHdfs:
    def __init__(self, hosts, user):
        self.hosts = hosts
        self.user = user
        self.client = pyhdfs.HdfsClient(hosts=self.hosts, user_name=self.user)
        
        print('目前环境可使用NameNode节点：')
        print(self.client.get_active_namenode())
    
    def list_dir(self, path, **kwargs):
        """
        返回目录下的所有文件，类似于 dfs -ls
        :param path: HDFS 路径地址
        """
        return self.client.listdir(path, **kwargs)
    
    def exists(self, path, **kwargs):
        """
        查看目录地址是否存在
        :param path: HDFS 路径地址
        """
        return self.client.exists(path)
    
    def list_status(self, path, **kwargs):
        # 获取文件或文件夹属性，通过type 区分文件与文件夹
        return self.client.list_status(path, **kwargs)
    
    def file_to_hdfs(self, linux_path, hdfs_path):
        """
        将 linux 文件上传至HDFS中，类似于 dfs -put
        :param linux_path: /home/project/tmp_file/1.zip
        :param hdfs_path: HDFS 文件夹地址， hdfs:/filehouse/file/
        :return: 返回源地址与HDFS地址
        """
        if os.path.isfile(linux_path):
            file_name = linux_path.split('/')[-1]
            hdfs_file = hdfs_path + file_name
            # hdfs_path 具体到文件名 /filehouse/file/pscp_test.zip
            f = open(linux_path, 'rb')
            self.client.create(hdfs_file, f, overwrite=True)
            # 返回源linux地址与HDFS地址
            
            return linux_path, hdfs_file
        
        elif os.path.isdir(linux_path):
            print("请提交具体的文件地址,而不是文件目录!")
        else:
            print("请提交具体的文件地址!")
    
    def folder_to_hdfs(self, linux_path, hdfs_path):
        """
        将文件夹及文件夹内所有文件
        :param linux_path:  /home/project/tmp_file/
        :param hdfs_path:  /filehouse/file/
        :return: 返回源地址与hdfs地址的字典
        """
        
        if not os.path.isdir(linux_path):
            print('请输入正确文件夹地址')
            return
        # 在HDFS 上新建文件夹用于集中存放这次数据集
        folder_name = linux_path.split('/')[-2]
        folder_name = hdfs_path + folder_name + '/'
        self.client.mkdirs(folder_name)
        
        # linux下所有文件的绝对地址
        file_names = []
        for dirpath, dirnames, filenames in os.walk(linux_path):
            for filename in filenames:
                file_names.append(os.path.join(dirpath, filename))
        
        file_dict = dict()
        for file_name in file_names:
            if os.path.isfile(file_name):
                add_address = file_name.split(linux_path)[-1]
                hdfs_file_address = folder_name + add_address
                self.client.create(hdfs_file_address, file_name, overwrite=True)
                # 加入字典
                file_dict[file_name] = hdfs_file_address
        
        return file_dict
        # 获取目录内所有文件，将子目录地址与文件名加到hdfs_path 变量上，再调用单个文件的上传命名
        # 可以自动生成前面的文件夹


class WinToLinux:
    """
    将 Windows 远程文件下载至Linux本地中
    :param win_host Window 远程ip地址
    :param win_user 登录名
    :param win_passwd 对应的登录密码
    :param port SSH端口，默认为22
    
    """
    
    def __init__(self, win_host, win_user, win_passwd,
                 linux_ip, linux_user, linux_passwd, port=22, ):
        self.win_host = win_host
        self.win_user = win_user
        self.win_passwd = win_passwd
        self.port = port
        
        self.linux_ip = linux_ip
        self.linux_user = linux_user
        self.linux_passwd = linux_passwd
        
        # 建立与window 系统的连接
        self.session = winrm.Session('http://{win_host}/wsman'.format(win_host=self.win_host),
                                     auth=(self.win_user, self.win_passwd))
        link_test = self.session.run_cmd('dir').status_code
        
        # 获取当前运行环境的IP地址
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        
        if link_test == 0:
            print('Connection Windows system successful !')
        else:
            print('Test unsuccessful, please check parameters !')
        if self.linux_ip == ip:
            pass
        else:
            print('Warning: Connected to another Linux environment !')
    
    def file_to_linux(self, win_path, linux_path):
        """
        将Windows下的文件，依据文件详细地址复制到Linux环境
        :param win_path: Windows下的文件地址，具体到文件名 F:/newspoon/pscp_test/111.zip
        :param linux_path: linux下的存储地址，具体到最后的实际存放路径 /home/project/tmp_file/
        :returns: 返回源文件名与转换后文件名
        """
        # print(' >>>>>>>>>> window_to_Linux file begin  >>>>>>>>>>')
        if not os.path.isdir(linux_path):
            os.mkdir(linux_path)
        cmd = 'pscp -pw {password} {window_path} {username}@{linux_ip}:{linux_path}'.format(
            password=self.linux_passwd, window_path=win_path, username=self.linux_user,
            linux_ip=self.linux_ip, linux_path=linux_path
        )
        
        res = self.session.run_cmd(cmd)
        
        file_name = win_path.split('/')[-1]
        linux_file_name = linux_path + file_name
        
        # return res and file address
        if res.status_code == 0:
            # 0 运行成功，记录源文件与转换文件名
            print(res.std_out.decode('gbk'))
            return win_path, linux_file_name
        else:
            print(res.std_err.decode('gbk'))
            return
    
    def folder_to_linux(self, win_path, linux_path, only_file=False):
        """
        将Windows 中的整个文件夹复制到linux环境
        :param win_path: Windows下的文件夹名称 F:/newspoon/pscp_test/
        :param linux_path: linux系统下，目标文件夹的存储路径 /home/project/tmp_file/
        :param only_file: 默认False，若为True则只传输文件夹内的所有文件
        """
        # 文件夹类型，pscp -r 递归传递，记录文件源地址与linux上的地址
        # print(' >>>>>>>>>> window_to_Linux folder begin  >>>>>>>>>>')
        # 情况一，只转移文件，不转移文件夹
        file_dict = dict()
        file_list = self.check_folder(win_path).split('\r\n')[:-1]
        # 传递到Linux上的文件集中存放在统一的同名文件夹里
        linux_path_add = linux_path + win_path.split('/')[-2] + '/'
        
        if only_file:
            for file in file_list:
                file = file.replace('\\', '/')
                # file_name = file.split('/')[-1]
                # linux_add = file.split(win_path)[-1].replace(file_name,'')
                # linux_address = linux_path + linux_add
                file_dict[file] = self.file_to_linux(file, linux_path_add)[1]
            
            return file_dict
        
        # 情况二，PSCP递归传递
        cmd = 'pscp -r -pw {password} {window_path} {username}@{linux_ip}:{linux_path}'.format(
            password=self.linux_passwd, window_path=win_path, username=self.linux_user,
            linux_ip=self.linux_ip, linux_path=linux_path_add
        )
        # 运行PSCP命令前，在linux环境补充存储目录，否则PSCP报找不到目录
        os.mkdir(linux_path_add)
        res = self.session.run_cmd(cmd)
        for file in file_list:
            file = file.replace('\\', '/')
            linux_add = file.split(win_path)[-1]
            file_dict[file] = linux_path_add + linux_add
        
        if res.status_code == 0:
            print(res.std_out.decode('gbk'))
            return file_dict
        else:
            return res.std_err.decode('gbk')
    
    def check_folder(self, folder_path):
        """
        查看Windows 地址下有哪些文件
        :return: 文件名称
        """
        # dir 的位置间隔符为\
        folder_path_tr = folder_path.replace('/', '\\')
        cmd = 'dir {win_path} /B /S /A:-D '.format(win_path=folder_path_tr)
        
        res = self.session.run_cmd(cmd)
        
        if res.status_code == 0:
            return res.std_out.decode('gbk')
        else:
            return res.std_err.decode('gbk')
    
    def check_is_dir(self, path):
        """
        判断地址是否为目录，True 为目录,False 为文件，Error 为出错
        :return: True OR False
        """
        dir_path = path.replace('/', '\\')
        cmd = 'dir {win_path} /B /S /A:-D '.format(win_path=dir_path)
        res = self.session.run_cmd(cmd)
        
        if res.status_code:
            return "Error"
        
        file_list = res.std_out.decode('gbk').split('\r\n')
        for file in file_list:
            file = file.replace('\\', '/')
            if file == path:
                return False
        return True
