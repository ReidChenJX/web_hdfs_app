#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/17 14:14
# @Author   : ReidChen
# Document  ：处理返回数据中，部门相关信息

import json

class department:
    """
    人员部门信息
    """
    def __init__(self):
        self.children = []
        self.dtCreate = None
        self.nmSort = 2
        self.stDeptCode = None
        self.stDeptId = "0d7806c3fd3f41ff8517efda5766a2d9"
        self.stDeptPid = "bfbaf4de07bb4746a2de22936cb9fe24"
        self.stDeptPids = "0,b43b2db088364f7eb7f5bb1686e2e610,bfbaf4de07bb4746a2de22936cb9fe24"
        self.stDeptname = "技术管理组"
        self.stLeader = "杨帅"
        self.stPhone = None
        self.stRemark = None
        self.stStatus = "0"
        self.stWorktel = None

    def ToJson(self):
        """将class属性转换json输出
        :return: json
        """
        deptInfo = {}
        deptInfo['children'] = self.children
        deptInfo['dtCreate'] = self.dtCreate
        deptInfo['nmSort'] = self.nmSort
        deptInfo['stDeptCode'] = self.stDeptCode
        deptInfo['stDeptId'] = self.stDeptId
        deptInfo['stDeptPid'] = self.stDeptPid
        deptInfo['stDeptPids'] = self.stDeptPids
        deptInfo['stDeptname'] = self.stDeptname
        deptInfo['stLeader'] = self.stLeader
        deptInfo['stPhone'] = self.stPhone
        deptInfo['stRemark'] = self.stRemark
        deptInfo['stStatus'] = self.stStatus
        deptInfo['stWorktel'] = self.stWorktel

        return deptInfo
        
    

dept = department()
deptInfo = dept.ToJson()