#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import json
import configparser
import os



IP = "http://dev-api.xxx.com"
USERNAME = "xxxx@xxxx.com"
PASSWORD = "xxxx"
COOKIE = ""


def login():
    global IP
    global COOKIE
    global USERNAME
    global PASSWORD
    url = IP + "/api/user/login_by_ldap"

    headers = {
        'Content-Type': "application/json",
    }

    body = {}
    body["email"] = USERNAME
    body["password"] = PASSWORD
    payload = json.dumps(body)

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)

    SetCookieByResponse = response.headers["Set-Cookie"].replace("httponly, ", "").replace(" ", "")
    SetCookieList = SetCookieByResponse.split(";")
    CookieList = []
    for item in SetCookieList:
        if item.split("=")[0] in {"_yapi_token", "UUID", "_yapi_uid"}:
            CookieList.append(item)

    COOKIE = ("; ").join(CookieList)


    return response.text


# 获取组列表
def group_list():
    global IP
    global COOKIE

    url = IP + "/api/group/list"

    headers = {
        'Cookie':  COOKIE,
    }
    response = requests.request("GET", url, headers=headers)

    # print(response.text)

    return response.text


def get_group_list_dict():
    response = group_list()
    groupList = json.loads(response)["data"]
    idDict = {}
    for item in groupList:
        idDict[item["_id"]] = item["group_name"]
    print(idDict)

    return idDict


# 获取项目列表
def project_list(group_id):
    global IP
    global COOKIE

    url = IP + "/api/project/list"

    headers = {
        'Cookie':  COOKIE,
    }


    body = {}
    body["group_id"] = group_id
    body["page"] = "1"
    body["limit"] = "500"
    querystring = body

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    return response.text



def get_project_list_dict(group_id):
    response = project_list(group_id)
    projectList = json.loads(response)["data"]["list"]
    idDict = {}
    for item in projectList:
        if item.get("name"):
            idDict[item["_id"]] = item["name"]
        elif item.get("projectid") and item.get("projectname"):
            idDict[item["projectid"]] = item["projectname"]



    print(idDict)

    return idDict


# 获取接口分组列表
def api_group(project_id):
    global IP
    global COOKIE

    url = IP + "/api/project/get"

    headers = {
        'Cookie':  COOKIE,
    }


    body = {}
    body["id"] = project_id
    querystring = body

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    return response.text



def get_api_group_dict(project_id):
    response = api_group(project_id)
    apiGroupList = json.loads(response)["data"]["cat"]
    idDict = {}
    for item in apiGroupList:
        idDict[item["_id"]] = item["name"]

    print(idDict)

    return idDict

def get_basepath_by_project(project_id):
    response = api_group(project_id)
    apiProjectInfo = json.loads(response)["data"]
    return apiProjectInfo["basepath"]



# 获取接口列表
def api_list(api_group_id):
    global IP
    global COOKIE

    url = IP + "/api/interface/list_cat"

    headers = {
        'Cookie':  COOKIE,
    }


    body = {}
    body["catid"] = api_group_id
    body["page"] = "1"
    body["limit"] = "500"
    querystring = body

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    return response.text



def get_api_list_dict(api_group_id):
    response = api_list(api_group_id)
    apiGroupList = json.loads(response)["data"]["list"]
    idDict = {}
    for item in apiGroupList:
        idDict[item["_id"]] = item["title"]

    print(idDict)

    return idDict


# 获取接口详情
def api_info(api_id):
    global IP
    global COOKIE

    url = IP + "/api/interface/get"

    headers = {
        'Cookie':  COOKIE,
    }


    body = {}
    body["id"] = api_id
    querystring = body

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    return response.text



def get_api_info(api_id):
    response = api_info(api_id)
    apiGroupInfo = json.loads(response)["data"]

    print(apiGroupInfo)

    return apiGroupInfo

def search(keywords):
    global IP
    global COOKIE

    url = IP + "/api/project/search"

    headers = {
        'Cookie':  COOKIE,
    }


    body = {}
    body["q"] = keywords
    querystring = body

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    return response.text


def get_search_project(keywords):
    response = search(keywords)
    apiGroupList = json.loads(response)["data"]["project"]
    idDict = {}
    for item in apiGroupList:
        idDict[item["_id"]] = item["name"]

    print(idDict)

    return idDict

#api详情转dict
def api_to_dict(URL, BASEPATH="", API_INFO={}):
    api = {}
    name = API_INFO["title"]

    request = {}

    method = API_INFO["method"]

    header = {}
    header_tmp_list = []
    for item in API_INFO["req_headers"]:
        header_tmp = {}
        header_tmp["key"] = item["name"]
        if item.get("value"):
            header_tmp["value"] = item["value"]
        else:
            header_tmp["value"] = ""
        header_tmp["type"] = "text"
        header_tmp_list.append(header_tmp)
        # print("header_tmp", header_tmp)
    # print("header_tmp_list", header_tmp_list)
    header = header_tmp_list

    body = {}
    mode = None
    formdata = []
    raw = ""
    if API_INFO.get("req_body_type") and API_INFO["req_body_type"] == "form":
        mode = "formdata"
        formdata_tmp_list = []
        for item in API_INFO["req_body_form"]:
            formdata_tmp = {}
            formdata_tmp["key"] = item["name"]
            if item.get("example"):
                formdata_tmp["value"] = item["example"]
            else:
                formdata_tmp["value"] = ""
            if item.get("desc"):
                formdata_tmp["description"] = item["desc"]
            else:
                formdata_tmp["description"] = ""
            formdata_tmp_list.append(formdata_tmp)
            # print("formdata_tmp", query_tmp)
            formdata = formdata_tmp_list

            body["mode"] = mode
            body["formdata"] = formdata

    elif API_INFO.get("req_body_type") and API_INFO["req_body_type"] == "json":
        mode = "raw"
        if API_INFO.get("req_body_other"):
            raw = API_INFO["req_body_other"]
        body["mode"] = mode
        body["raw"] = raw

    url = {}
    # raw = None

    protocol = ""
    host = []
    if len(URL.split("://")) == 1:
        host = URL.strip().split("://")[0].split(".")
    elif len(URL.split("://")) >= 1:
        protocol = URL.strip().split("://")[0]
        host = URL.strip().split("://")[1].split(".")

    path = BASEPATH + API_INFO["path"]
    query = {}
    query_tmp_list = []
    for item in API_INFO["req_query"]:
        query_tmp = {}
        query_tmp["key"] = item["name"]
        if item.get("example"):
            query_tmp["value"] = item["example"]
        else:
            query_tmp["value"] = ""
        query_tmp["description"] = item["desc"]
        query_tmp_list.append(query_tmp)
        # print("query_tmp", query_tmp)
    query = query_tmp_list
    # print("query_tmp_list", query_tmp_list)
    # url["raw"] = raw
    url["protocol"] = protocol
    url["host"] = host
    url["path"] = path
    url["query"] = query

    request["method"] = method
    request["header"] = header
    request["body"] = body
    request["url"] = url

    api["name"] = name
    api["request"] = request
    api["response"] = []

    print(api)
    # print(json.dumps(api))

    return api


#api详情转dict
def api_list_to_dict(NAME, API_LIST, isROOT=False):

    api_list = {}

    info = {}

    if isROOT:
        info["_postman_id"] = "coding by chen"
        info["name"] = NAME
        info["schema"] = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"

        api_list["info"] = info
        api_list["item"] = API_LIST
    else:
        api_list["name"] = NAME
        api_list["item"] = API_LIST

    print(api_list)
    # print(json.dumps(api_list))

    return api_list

#转postman格式字符串
def api_list_to_postman(API_LIST):
    postman = json.dumps(API_LIST, sort_keys=True, indent=4, separators=(',', ':'))
    return postman

# 写入文件
def export_postman(API_JSON, FILE_PATH):
    f = open(FILE_PATH, 'w', encoding='utf8')
    f.write(API_JSON)
    f.close()
