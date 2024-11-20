from db.sql_manager import SQLManager

mitu_tool = SQLManager('mitu_tool')


# 查询多条数据
def get_list():
    sql = ("select id,name,user_id,ip,mobile,"
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time,"
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s')  as update_time from user_info")
    data = mitu_tool.get_list(sql)
    return data


# 查询单条数据
def get_one_by_user_id(user_id):
    sql = ("select id,name,user_id,ip,mobile,DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time,"
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s')  as update_time from user_info "
           "where user_id ='{}'").format(str(user_id))
    data = mitu_tool.get_one(sql)
    return data


def save_user_info(user_id, name, ip, mobile):
    """
    保存新用户信息到user_info表
    """
    sql = "INSERT INTO user_info (user_id, name, ip, mobile, created_time) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
    args = (user_id, name, ip, mobile)
    return mitu_tool.create(sql, args)


def update_user_info(user_id, name=None, ip=None, mobile=None):
    """
    根据用户ID修改用户信息
    """
    update_fields = []
    update_values = []

    if name is not None:
        update_fields.append("name = %s")
        update_values.append(name)
    if ip is not None:
        update_fields.append("ip = %s")
        update_values.append(ip)
    if mobile is not None:
        update_fields.append("mobile = %s")
        update_values.append(mobile)

    if not update_fields:
        raise ValueError("至少需要提供一个要更新的字段值。")

    update_fields_str = ", ".join(update_fields)
    sql = f"UPDATE user_info SET {update_fields_str}, updated_time = CURRENT_TIMESTAMP WHERE user_id = '{user_id}'"
    args = tuple(update_values)

    mitu_tool.moddify(sql, args)


if __name__ == '__main__':
    # print(save_user_info("1234562", 'test', '127.0.0.1', '123456789'))
    print(update_user_info(1234562, 'test', '127.0.0.1', '11111111'))
    print(get_one_by_user_id('1234562'))
