#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/17 11:40
# @Author   : ReidChen
# Document  ：集中处理网页菜单与权限功能


import json

class menu_sing:
    """
    根据人员ID，单个目录
    """
    def __init__(self):
        self.children = []
        self.nmSort = 0
        self.stIcon = None
        self.stIslink = ""
        self.stMenuId = ""
        self.stMenuName = ""
        self.stMenuPid = ""
        self.stPerms = ""
        self.stRemark = ""
        self.stStatus = ""
        self.stType = ""
        self.stUrl = ""
        
    def ToJson(self):
        """将class属性转换json输出
        :return: json
        """
        meun_dict = {}
        meun_dict['children'] = self.children
        meun_dict['nmSort'] = self.nmSort
        meun_dict['stIcon'] = self.stIcon
        meun_dict['stIslink'] = self.stIslink
        meun_dict['stMenuId'] = self.stMenuId
        meun_dict['stMenuName'] = self.stMenuName
        meun_dict['stMenuPid'] = self.stMenuPid
        meun_dict['stPerms'] = self.stPerms
        meun_dict['stRemark'] = self.stRemark
        meun_dict['stStatus'] = self.stStatus
        meun_dict['stStatus'] = self.stStatus
        meun_dict['stType'] = self.stType
        meun_dict['stUrl'] = self.stUrl
        
        return meun_dict
        
    def getDataFill(self, **keys):
        """
        数据库获取
        """
        
        
        pass
    
## 测试、临时目录结构
obj_1 = menu_sing()
obj_2_chi_1 = menu_sing()
obj_2_chi_2 = menu_sing()
obj_2 = menu_sing()
obj_3 = menu_sing()
obj_4 = menu_sing()
obj_5 = menu_sing()

# obj_1 内容
obj_1.children = []
obj_1.nmSort = 0
obj_1.stIcon = None
obj_1.stIslink = "0"
obj_1.stMenuId = "aaeb05744ec34cf5985d4437582579f6"
obj_1.stMenuName = "首页"
obj_1.stMenuPid = "0"
obj_1.stPerms = "home:view"
obj_1.stRemark = None
obj_1.stStatus = "0"
obj_1.stType = "menu"
obj_1.stUrl = "/home"
mun_list_obj_1 = obj_1.ToJson()

# obj_2_chi_1 内容
obj_2_chi_1.children = []
obj_2_chi_1.nmSort = 0
obj_2_chi_1.stIcon = None
obj_2_chi_1.stIslink = "0"
obj_2_chi_1.stMenuId = "bbc82bca7eb54bbaa2e32bf24310486e"
obj_2_chi_1.stMenuName = "用户管理"
obj_2_chi_1.stMenuPid = "g8s1798ea4d84e8bb1ddd2ec8cd50br9"
obj_2_chi_1.stPerms = "system:user"
obj_2_chi_1.stRemark = None
obj_2_chi_1.stStatus = "0"
obj_2_chi_1.stType = "menu"
obj_2_chi_1.stUrl = "/system/user"
mun_list_obj_2_chi_1= obj_2_chi_1.ToJson()

# obj_2_chi_2 内容
obj_2_chi_2.children = []
obj_2_chi_2.nmSort = 1
obj_2_chi_2.stIcon = None
obj_2_chi_2.stIslink = "0"
obj_2_chi_2.stMenuId = "3f58b55ace314996a4957694fcefdc8f"
obj_2_chi_2.stMenuName = "部门管理"
obj_2_chi_2.stMenuPid = "g8s1798ea4d84e8bb1ddd2ec8cd50br9"
obj_2_chi_2.stPerms = "system:dept"
obj_2_chi_2.stRemark = None
obj_2_chi_2.stStatus = "0"
obj_2_chi_2.stType = "menu"
obj_2_chi_2.stUrl = "/system/dept"
mun_list_obj_2_chi_2= obj_2_chi_2.ToJson()




# obj_2 内容
obj_2.children = [mun_list_obj_2_chi_1,mun_list_obj_2_chi_2]
obj_2.nmSort = 1
obj_2.stIcon = None
obj_2.stIslink = "0"
obj_2.stMenuId = "g8s1798ea4d84e8bb1ddd2ec8cd50br9"
obj_2.stMenuName = "系统管理"
obj_2.stMenuPid = "0"
obj_2.stPerms = ""
obj_2.stRemark = None
obj_2.stStatus = "0"
obj_2.stType = "menu"
obj_2.stUrl = "#"
mun_list_obj_2 = obj_2.ToJson()





# obj_3 内容
obj_3.children = []
obj_3.nmSort = 2
obj_3.stIcon = None
obj_3.stIslink = "0"
obj_3.stMenuId = "ce18c6ce02c54782ae56d427cce776c3"
obj_3.stMenuName = "日志管理"
obj_3.stMenuPid = "0"
obj_3.stPerms = "system:log"
obj_3.stRemark = None
obj_3.stStatus = "0"
obj_3.stType = "menu"
obj_3.stUrl = ""
mun_list_obj_3 = obj_3.ToJson()

# obj_4 内容
obj_4.children = []
obj_4.nmSort = 3
obj_4.stIcon = None
obj_4.stIslink = "0"
obj_4.stMenuId = "62d7fdd043484fa5880973b0b552b070"
obj_4.stMenuName = "管理页面"
obj_4.stMenuPid = "0"
obj_4.stPerms = "manage:view"
obj_4.stRemark = None
obj_4.stStatus = "0"
obj_4.stType = "menu"
obj_4.stUrl = "/manage"
mun_list_obj_4 = obj_4.ToJson()


# obj_5 内容
obj_5.children = []
obj_5.nmSort = 4
obj_5.stIcon = None
obj_5.stIslink = "0"
obj_5.stMenuId = "2ecd2c8ab4ed462cb3906c87f8a6cbb4"
obj_5.stMenuName = "系统工具"
obj_5.stMenuPid = "0"
obj_5.stPerms = "system:tool"
obj_5.stRemark = None
obj_5.stStatus = "0"
obj_5.stType = "menu"
obj_5.stUrl = "/tool"
mun_list_obj_5 = obj_5.ToJson()

menuList = [mun_list_obj_1, mun_list_obj_2, mun_list_obj_3,
            mun_list_obj_4, mun_list_obj_5]



