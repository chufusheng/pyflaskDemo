from db.sql_manager import SQLManager

mitu_tool = SQLManager('mitu_tool')


# 查询多条产品信息数据
def get_product_info_list():
    sql = ("select id, product_key, product_name, amount, status, product_yunshi, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time "
           "from product_info")
    data = mitu_tool.get_list(sql)
    return data


# 查询单条产品信息数据
def get_one_product_info_by_product_key(product_key):
    sql = ("select id, product_key, product_name, amount, status, product_yunshi, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time, "
           "DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') as updated_time "
           "from product_info "
           "where product_key ='{}'").format(str(product_key))
    data = mitu_tool.get_one(sql)
    return data


def save_product_info(product_key, product_name, amount, status, product_yunshi):
    """
    保存新的产品信息到product_info表
    """
    sql = ("INSERT INTO product_info (product_key, product_name, amount, status, product_yunshi, created_time) VALUES "
           "(%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)")
    args = (product_key, product_name, amount, status, product_yunshi)
    return mitu_tool.create(sql, args)


def update_product_info(product_key, product_name=None, amount=None, status=None, product_yunshi=None):
    """
    根据产品键修改产品信息
    """
    update_fields = []
    update_values = []

    if product_name is not None:
        update_fields.append("product_name = %s")
        update_values.append(product_name)
    if amount is not None:
        update_fields.append("amount = %s")
        update_values.append(amount)
    if status is not None:
        update_fields.append("status = %s")
    update_values.append(status)
    if product_yunshi is not None:
        update_fields.append("product_yunshi = %s")
        update_values.append(product_yunshi)

    if not update_fields:
        raise ValueError("至少需要提供一个要更新的字段值。")

    update_fields_str = ", ".join(update_fields)
    sql = f"UPDATE product_info SET {update_fields_str}, updated_time = CURRENT_TIMESTAMP WHERE product_key = {product_key}"
    args = tuple(update_values)

    mitu_tool.modify(sql, args)



if __name__ == '__main__':
    print(save_product_info('123456', '姻缘测试', 100, 1, '哈哈哈哈'))
    print(get_product_info_list())