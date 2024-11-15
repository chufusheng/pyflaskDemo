import json
import math

import requests

from db.sql_manager import SQLManager

tool_app = SQLManager('tool_app')


# 查询多条数据
def get_list():
    sql = "select id,source_name,account_name,password_str,mark," \
          "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time," \
          "DATE_FORMAT(update_time, '%Y-%m-%d %H:%i:%s')  as update_time from password_info"
    data = tool_app.get_list(sql)
    # tool_app.close()
    return data


# 查询单条数据
def get_one_by_id(id):
    sql = "select id,account_name,password_str,mark," \
          "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time," \
          "DATE_FORMAT(update_time, '%Y-%m-%d %H:%i:%s')  as update_time from password_info  " \
          "where id ={}".format(str(id))
    data = tool_app.get_one(sql)
    # tool_app.close()
    return data


def pass_add(data):
    account_name = data['account_name']
    password_str = data['password_str']
    mark = data['mark']
    source_name = data['source_name']

    sql = "INSERT INTO password_info (source_name,account_name, password_str, mark)" \
          "VALUES ('{source_name}','{account_name}','{password_str}', '{mark}')" \
        .format(source_name=source_name, account_name=account_name, password_str=password_str, mark=mark)
    data = tool_app.create(sql)
    # tool_app.close()
    return data


def pass_update(data):
    id = data['id']
    account_name = data['account_name']
    password_str = data['password_str']
    mark = data['mark']
    source_name = data['source_name']

    sql = "UPDATE password_info SET source_name='{source_name}'," \
          "account_name='{account_name}',password_str= '{password_str}',mark= '{mark}' " \
          "WHERE id = {id}".format(id=int(id), source_name=source_name, account_name=account_name,
                                   password_str=password_str, mark=mark)
    data = tool_app.moddify(sql)
    # tool_app.close()

    return data


#
# if __name__ == '__main__':
    # print(get_list())
