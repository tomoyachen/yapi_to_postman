#!/usr/bin/python
# -*- coding: utf-8 -*-

import controller
import os

# URL = "{{IP}}"
URL = "https://t-ijx.xxxx.com"
YAPI_PROJECT = "izj-xxxx"
FILE_PATH = "E:\\Desktop"


def login():
    controller.login()

#导出一个文件，以组分组
def export_project_to_postman(YAPI_PROJECT):
    #搜索项目名后进行遍历
    keywords = YAPI_PROJECT
    api_group_list = controller.get_search_project(keywords)
    if len(api_group_list) > 1:
        print("查询结果过多，请输入完整项目名查询！", api_group_list)
    elif len(api_group_list) < 1:
        print("查询结果为空！")
    else:
        list = []

        for key, value in api_group_list.items():
            project_key = key
            project_value = value
        # 接口分组
        api_group_list = controller.get_api_group_dict(project_id=project_key)
        for api_group_key, api_group_value in api_group_list.items():
            print(api_group_key, api_group_value)

            group_list = []
            # 接口列表
            api_list = controller.get_api_list_dict(api_group_id=api_group_key)
            for api_key, api_value in api_list.items():
                print(api_key, api_value)

                # 接口详情
                api_info = controller.get_api_info(api_id=api_key)
                api = controller.api_to_dict(URL = URL, API_INFO = api_info)
                group_list.append(api)
            api_group_dict = controller.api_list_to_dict(NAME=api_group_value, API_LIST=group_list)
            list.append(api_group_dict)
        api_list_dict = controller.api_list_to_dict(NAME=project_value, API_LIST=list, isROOT=True)
        postman = controller.api_list_to_postman(api_list_dict)
        controller.export_postman(API_JSON=postman, FILE_PATH=FILE_PATH + "\\" + project_value + ".postman_collection.json")


#导出多个文件，每个文件是一个分组
def export_api_to_postman(YAPI_PROJECT):
    #搜索项目名后进行遍历
    keywords = YAPI_PROJECT
    api_group_list = controller.get_search_project(keywords)
    if len(api_group_list) > 1:
        print("查询结果过多，请输入完整项目名查询！", api_group_list)
    elif len(api_group_list) < 1:
        print("查询结果为空！")
    else:
        list = []

        for key, value in api_group_list.items():
            project_key = key
            project_value = value

        if os.path.exists(FILE_PATH + "\\" + "Postman_" + project_value):
            pass
        else:
            os.mkdir(FILE_PATH + "\\" +  project_value + "_Postman")

        # 接口分组
        api_group_list = controller.get_api_group_dict(project_id=project_key)
        for api_group_key, api_group_value in api_group_list.items():
            print(api_group_key, api_group_value)

            group_list = []
            # 接口列表
            api_list = controller.get_api_list_dict(api_group_id=api_group_key)
            for api_key, api_value in api_list.items():
                print(api_key, api_value)

                # 接口详情
                api_info = controller.get_api_info(api_id=api_key)
                api = controller.api_to_dict(URL = URL, API_INFO = api_info)
                group_list.append(api)
            api_group_dict = controller.api_list_to_dict(NAME=api_group_value, API_LIST=group_list, isROOT=True)
            postman = controller.api_list_to_postman(api_group_dict)
            controller.export_postman(API_JSON=postman, FILE_PATH=FILE_PATH + "\\" + "Postman_" + project_value + "\\" + api_group_value + ".postman_collection.json")



login()
# export_project_to_postman(YAPI_PROJECT)
export_api_to_postman(YAPI_PROJECT)
export_api_to_postman("demo")


# controller.login()

# controller.get_group_list_dict()
#
# controller.get_project_list_dict(group_id=225)

# controller.get_api_group_dict(57)
#
#
# controller.get_api_list_dict(84)
#
# controller.get_api_info(268)
#


'''
# 大组
# 完全遍历
group_list = controller.get_group_list_dict()
for group_key, group_value in group_list.items():
    print(group_key, group_value)

    # 项目
    project_list = controller.get_project_list_dict(group_id=group_key)
    for project_key, project_value in project_list.items():
        print(project_key, project_value)

        # 接口分组
        api_group_list = controller.get_api_group_dict(project_id=project_key)
        for api_group_key, api_group_value in api_group_list.items():
            print(api_group_key, api_group_value)

            # 接口列表
            api_list = controller.get_api_list_dict(api_group_id=api_group_key)
            for api_key, api_value in api_list.items():
                print(api_key, api_value)

                # 接口详情
                api_info = controller.get_api_info(api_id=api_key)
                for api_info_key, api_info_value in api_info.items():
                    print(api_info_key, api_info_value)
                    # break;

'''

'''
#搜索项目名后进行遍历
api_group_list = controller.get_search_project("ixs-hfjy")
if len(api_group_list) > 1:
    print("查询结果过多，请输入完整项目名查询！", api_group_list)
elif len(api_group_list) < 1:
    print("查询结果为空！")
else:
    for key, value in api_group_list.items():
        project_key = key
    # 接口分组
    api_group_list = controller.get_api_group_dict(project_id=project_key)
    for api_group_key, api_group_value in api_group_list.items():
        print(api_group_key, api_group_value)

        # 接口列表
        api_list = controller.get_api_list_dict(api_group_id=api_group_key)
        for api_key, api_value in api_list.items():
            print(api_key, api_value)

            # 接口详情
            api_info = controller.get_api_info(api_id=api_key)
            for api_info_key, api_info_value in api_info.items():
                print(api_info_key, api_info_value)
                break;
'''


# # 测试代码
# api_info = controller.get_api_info(268)
# api = controller.api_to_dict(HTTP = "https", URL = "test-cwshenpi.hfjy.com", API_INFO = api_info)
# api_list = controller.api_list_to_dict(NAME = "APIIII", API_LIST= [api, api])
# postman = controller.api_list_to_postman(api_list)
# controller.export_postman(API_JSON = postman, FILE_PATH = "E:\\Desktop\\aaa.postman_collection.json")
