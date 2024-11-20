from datetime import datetime

from db.sql_manager import SQLManager

mitu_tool = SQLManager('mitu_tool')


# 查询多条订单数据
def get_order_list():
    sql = ("select id, user_id, order_no, amount, status, "
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time, "
           "user_name,user_birthday,birthday_hour,user_gender,product_id, product_name, yunshi "
           "from order_info")
    data = mitu_tool.get_list(sql)
    return data


# 查询单条数据
def get_order_list_by_user_id(user_id):
    sql = ("select id, user_id, order_no, amount, status, "
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time, "
           "user_name,user_birthday,birthday_hour,user_gender,product_id, product_name, yunshi,yunshi_status "
           "from order_info "
           "where user_id ='{}'").format(str(user_id))
    data = mitu_tool.get_list(sql)
    return data


# 查询单条数据
def get_one_order_by_order_no(order_no):
    sql = ("select id, user_id, order_no, amount, status,"
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time, "
           "user_name,user_birthday,birthday_hour,user_gender,product_id, product_name, yunshi,yunshi_status "
           "from order_info where order_no ='{}'").format(str(order_no))
    data = mitu_tool.get_one(sql)
    return data


def save_order_info(user_id, order_no, amount, status, pay_time, product_id, user_name, user_birthday, birthday_hour,
                    user_gender, product_name, yunshi, yunshi_status, ip):
    """
    保存新订单信息到order_info表
    """
    sql = (
        "INSERT INTO order_info (user_id, order_no, amount, status, pay_time, product_id, product_name,user_name,"
        "user_birthday,birthday_hour,user_gender,yunshi, yunshi_status,ip) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)")
    args = (
        user_id, order_no, amount, status, pay_time, product_id, product_name, user_name, user_birthday, birthday_hour,
        user_gender, yunshi, yunshi_status, ip)
    return mitu_tool.create(sql, args)


def update_order_info(order_no=None, amount=None, status=None, pay_time=None, product_id=None,
                      product_name=None, yunshi=None, yunshi_status=None):
    """
    根据用户ID修改订单信息
    """
    update_fields = []
    update_values = []

    if amount is not None:
        update_fields.append("amount = %s")
        update_values.append(amount)
    if status is not None:
        update_fields.append("status = %s")
        update_values.append(status)
    if pay_time is not None:
        update_fields.append("pay_time = %s")
        update_values.append(pay_time)
    if product_id is not None:
        update_fields.append("product_id = %s")
        update_values.append(product_id)
    if product_name is not None:
        update_fields.append("product_name = %s")
        update_values.append(product_name)
    if yunshi is not None:
        update_fields.append("yunshi = %s")
        update_values.append(yunshi)
    if yunshi_status is not None:
        update_fields.append("yunshi_status = %s")
        update_values.append(yunshi_status)

    if not update_fields:
        raise ValueError("至少需要提供一个要更新的字段值。")

    update_fields_str = ", ".join(update_fields)
    sql = f"UPDATE order_info SET {update_fields_str} WHERE order_no = '{order_no}'"
    args = tuple(update_values)

    mitu_tool.moddify(sql, args)


if __name__ == '__main__':
    # print(save_user_info("1234562", 'test', '127.0.0.1', '123456789'))
    # print(update_user_info(1234562, 'test', '127.0.0.1', '11111111'))
    # print(get_one_by_user_id('1234562'))
    # print(save_order_info("1234562", '123456', 100, 1, '2024-11-18 19:42:33', 1, '测试商品', '沙发发啊大大八十多'))
    # update_order_info('123456',  10000, 1, '2024-11-18 19:42:33', 1, '测试商品', '沙发发啊大大八十多')
    update_order_info(order_no='f65116ef1b7d4cdd', pay_time=datetime.now(),status=3)
    print(get_order_list())
    # print(get_order_list_by_user_id('fwqerew'))
