from db.sql_manager import SQLManager

mitu_tool = SQLManager('mitu_tool')


# 查询多条支付信息数据
def get_pay_info_list():
    sql = ("select id, pay_id, status, order_no, "
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time "
           "from pay_info")
    data = mitu_tool.get_list(sql)
    return data


# 查询单条支付信息数据
def get_list_pay_info_by_order_no(order_no):
    sql = ("select id, pay_id, status, order_no, "
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time "
           "from pay_info "
           "where order_no ={}").format(str(order_no))
    data = mitu_tool.get_list(sql)
    return data


def get_one_pay_info_by_pay_id(order_no):
    sql = ("select id, pay_id, status, order_no, "
           "DATE_FORMAT(pay_time, '%Y-%m-%d %H:%i:%s') as pay_time, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time "
           "from pay_info "
           "where order_no ={}").format(str(order_no))
    data = mitu_tool.get_list(sql)
    return data

def save_pay_info(pay_id, pay_time, status, order_no):
    """
    保存新支付信息到pay_info表
    """
    sql = (
        "INSERT INTO pay_info (pay_id, pay_time, status, order_no, created_time) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)")
    args = (pay_id, pay_time, status, order_no)
    return mitu_tool.create(sql, args)


def update_pay_info(pay_id=None, pay_time=None, status=None):
    """
    根据订单编号修改支付信息
    """
    update_fields = []
    update_values = []

    if pay_time is not None:
        update_fields.append("pay_time = %s")
        update_values.append(pay_time)
    if status is not None:
        update_fields.append("status = %s")
        update_values.append(status)

    if not update_fields:
        raise ValueError("至少需要提供一个要更新的字段值。")

    update_fields_str = ", ".join(update_fields)
    sql = f"UPDATE pay_info SET {update_fields_str}, updated_time = CURRENT_TIMESTAMP WHERE pay_id = {pay_id}"
    args = tuple(update_values)

    mitu_tool.moddify(sql, args)

if __name__ == '__main__':
    # save_pay_info(1, '2019-09-09 09:09:09', 1, 1)
    update_pay_info(pay_id=1, pay_time='2020-09-09 09:09:09',status=2)
    print(get_pay_info_list())
    print(get_list_pay_info_by_order_no(1))

