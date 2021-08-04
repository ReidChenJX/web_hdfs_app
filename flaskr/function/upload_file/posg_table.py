#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/15 10:39
# @Author   : ReidChen
# Document  ：Postgresql 链接,执行SQL操作


from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()


class TableStructure(Base):
    # 通过 declarative_base 类进行表单声明
    # 表名称
    __tablename__ = 'winfile_to_hdfs'
    
    # 表结构
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    is_record = Column(String(4), nullable=False)
    database_source = Column(String(250), nullable=True)
    win_file = Column(String(250), nullable=False, unique=True)
    hdfs_file = Column(String(250), nullable=False)
    create_time = Column(String(20), nullable=False)


class WinHdfsTable:
    
    def __init__(self, ip, port, user, passwd, database):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        
        # 初始化链接
        self.engine = create_engine('postgresql+psycopg2://{user}:{passwd}@{ip}:{port}/{database}'.format(
            user=self.user, passwd=self.passwd, ip=self.ip, port=self.port, database=self.database
        ))
        self.DBSession = sessionmaker(bind=self.engine)
    
    def create_table(self):
        Base.metadata.create_all(self.engine, checkfirst=True)
    
    def insert_data(self, data_dict, is_record=0, database_source=None):
        """
        :param data_dict: win文件地址与hdfs文件地址对应关系
        :param is_record: 在数据库中是否有记载（1为记载），若有则需要记录数据库中记载的源地址
        :param database_source: win文件地址与数据库记录地址对应关系
        """
        # 实例化一个会话类
        session = self.DBSession()
        # 定义上传时间
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #
        if is_record == 1:
            database_source = database_source
        else:
            database_source = dict([(k, []) for k in data_dict])  # 空字典
        # 对传入的字典数据进行解析
        for win_file, hdfs_file in data_dict.items():
            database_source_value = database_source[win_file]
            # 空字典在数据库中显示为{}，修改为None
            if len(database_source_value) == 0:
                database_source_value = None
            # 判断是更新还是插入新数据
            up_data = session.query(TableStructure).filter_by(win_file=win_file).first()
            if up_data:
                up_data.hdfs_file = hdfs_file
                up_data.create_time = local_time
                session.add(up_data)
            else:
                new_data = TableStructure(is_record=is_record, win_file=win_file, database_source=database_source_value,
                                          hdfs_file=hdfs_file, create_time=local_time)
                session.add(new_data)
        # 提交修改数据
        session.commit()
        session.close()
    
    def select_data(self, win_file):
        """
        :param win_file: win系统下文件地址，根据此地址查询数据是否有记录
        :return: None Or True
        """
        # 查询操作 常规操作，后续需修改
        session = self.DBSession()
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(TableStructure).filter(TableStructure.id == '1' and TableStructure.name == 'hsh4').one()
        print('name:', user.name)
        print('id_address:', user.id_address)
        session.close()
    
    def updateData(self, data_dict, is_record=0, database_source=None):
        # 更新操作,后续需修改
        session = self.DBSession()  # 创建会话
        users = session.query(TableStructure).filter_by(name="hsh4").first()  # 查询条件
        users.id_number = "abcd"  # 更新操作
        session.add(users)  # 添加到会话
        session.commit()  # 提交即保存到数据库
        session.close()
    
    def deleteData(self):
        # 删除操作,后续需修改
        session = self.DBSession()  # 创建会话
        delete_users = session.query(TableStructure).filter(TableStructure.id == "1").first()
        if delete_users:
            session.delete(delete_users)
            session.commit()
        session.close()  # 关闭会话
