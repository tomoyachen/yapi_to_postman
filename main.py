#!/usr/bin/python
# -*- coding: utf-8 -*-

import controller
import os
import sys


URL = "{{IP}}"
# URL = "https://t-xxxx.xxxx.com"
YAPI_PROJECT = "demo"
FILE_PATH = "E:\\Desktop"

try:
    YAPI_PROJECT = sys.argv[1]
except Exception:
    pass

try:
    FILE_PATH = sys.argv[2]
except Exception:
    pass

try:
    URL = sys.argv[3]
except Exception:
    pass

print ("YAPI 项目名: ", YAPI_PROJECT)
print ("导出路径: ", FILE_PATH)
print ("域名: ", URL)
print("--------------------开始导出--------------------")


def login():
    controller.login()

#导出一个文件，以组分组
def export_project_to_postman(YAPI_PROJECT):
    #搜索项目名后进行遍历
    keywords = YAPI_PROJECT
    api_group_list = controller.get_search_project(keywords)
    if len(api_group_list) > 1:
        print("查询结果过多，请输入完整项目名查询！")
        print("--------------------导出失败--------------------")
    elif len(api_group_list) < 1:
        print("查询结果为空！")
        print("--------------------导出失败--------------------")
    else:
        list = []

        for key, value in api_group_list.items():
            project_key = key
            project_value = value
        # 接口分组
        api_group_list = controller.get_api_group_dict(project_id=project_key)
        api_basepath = controller.get_basepath_by_project(project_id=project_key)
        for api_group_key, api_group_value in api_group_list.items():
            print(api_group_key, api_group_value)

            group_list = []
            # 接口列表
            api_list = controller.get_api_list_dict(api_group_id=api_group_key)
            for api_key, api_value in api_list.items():
                print(api_key, api_value)

                # 接口详情
                api_info = controller.get_api_info(api_id=api_key)
                api = controller.api_to_dict(URL = URL, BASEPATH=api_basepath, API_INFO = api_info)
                group_list.append(api)
            api_group_dict = controller.api_list_to_dict(NAME=api_group_value, API_LIST=group_list)
            list.append(api_group_dict)
        api_list_dict = controller.api_list_to_dict(NAME=project_value, API_LIST=list, isROOT=True)
        postman = controller.api_list_to_postman(api_list_dict)
        controller.export_postman(API_JSON=postman, FILE_PATH=FILE_PATH + "\\" + project_value + ".postman_collection.json")
        print("--------------------导出成功--------------------")

#导出多个文件，每个文件是一个分组
def export_api_to_postman(YAPI_PROJECT):
    #搜索项目名后进行遍历
    keywords = YAPI_PROJECT
    api_group_list = controller.get_search_project(keywords)
    if len(api_group_list) > 1:
        print("查询结果过多，请输入完整项目名查询！")
        print("--------------------导出失败--------------------")
    elif len(api_group_list) < 1:
        print("查询结果为空！")
        print("--------------------导出失败--------------------")
    else:
        list = []

        for key, value in api_group_list.items():
            project_key = key
            project_value = value

        if os.path.exists(FILE_PATH + "\\" + "Postman_" + project_value):
            pass
        else:
            os.mkdir(FILE_PATH + "\\" + "Postman_" + project_value)

        # 接口分组
        api_group_list = controller.get_api_group_dict(project_id=project_key)
        api_basepath = controller.get_basepath_by_project(project_id=project_key)
        for api_group_key, api_group_value in api_group_list.items():
            print(api_group_key, api_group_value)

            group_list = []
            # 接口列表
            api_list = controller.get_api_list_dict(api_group_id=api_group_key)
            for api_key, api_value in api_list.items():
                print(api_key, api_value)

                # 接口详情
                api_info = controller.get_api_info(api_id=api_key)
                api = controller.api_to_dict(URL = URL, BASEPATH=api_basepath, API_INFO = api_info)
                group_list.append(api)
            api_group_dict = controller.api_list_to_dict(NAME=api_group_value, API_LIST=group_list, isROOT=True)
            postman = controller.api_list_to_postman(api_group_dict)
            controller.export_postman(API_JSON=postman, FILE_PATH=FILE_PATH + "\\" + "Postman_" + project_value + "\\" + api_group_value + ".postman_collection.json")

        print("--------------------导出成功--------------------")


login()
# export_project_to_postman(YAPI_PROJECT)
export_api_to_postman(YAPI_PROJECT)

