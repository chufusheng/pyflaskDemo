from db.sql_manager import SQLManager

mitu_tool = SQLManager('mitu_tool')


# 查询所有股票数据记录
def get_stock_scrapy_record_list():
    sql = ("SELECT id, stock_code, scrapy_time, price, price_increase, price_percent, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time "
           "FROM stock_scrapy_record")
    data = mitu_tool.get_list(sql)
    return data


# 根据股票代码查询单条股票数据记录
def get_stock_scrapy_record_by_stock_code(stock_code):
    sql = ("SELECT id, stock_code, scrapy_time, price, price_increase, price_percent, "
           "DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') as created_time "
           "FROM stock_scrapy_record "
           "WHERE stock_code = '{}'").format(str(stock_code))
    data = mitu_tool.get_one(sql)
    return data


# 保存新的股票数据记录
def save_stock_scrapy_record(stock_code, scrapy_time, price, price_increase, price_percent):
    """
    保存新的股票数据记录到stock_scrapy_record表
    """
    sql = ("INSERT INTO stock_scrapy_record (stock_code, scrapy_time, price, price_increase, price_percent, created_time) "
           "VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)")
    args = (stock_code, scrapy_time, price, price_increase, price_percent)
    return mitu_tool.create(sql, args)


# 更新股票数据记录
def update_stock_scrapy_record(stock_code, price=None, price_increase=None, price_percent=None):
    """
    根据股票代码修改股票数据记录
    """
    update_fields = []
    update_values = []

    if price is not None:
        update_fields.append("price = %s")
        update_values.append(price)
    if price_increase is not None:
        update_fields.append("price_increase = %s")
        update_values.append(price_increase)
    if price_percent is not None:
        update_fields.append("price_percent = %s")
        update_values.append(price_percent)

    if not update_fields:
        raise ValueError("至少需要提供一个要更新的字段值。")

    update_fields_str = ", ".join(update_fields)
    sql = f"UPDATE stock_scrapy_record SET {update_fields_str}, created_time = CURRENT_TIMESTAMP WHERE stock_code = {stock_code}"
    args = tuple(update_values)

    mitu_tool.moddify(sql, args)


if __name__ == '__main__':
    # 测试插入数据
    # print(save_stock_scrapy_record('600000', '2024-12-05 09:30:00', '15.50', '+0.10', '+0.65%'))

    # 测试查询所有数据
    print(get_stock_scrapy_record_list())

    # 测试根据股票代码查询数据
    print(get_stock_scrapy_record_by_stock_code('600000'))

    # 测试更新股票数据记录
    print(update_stock_scrapy_record('600000', price='16.00', price_increase='+0.20', price_percent='+1.25%'))
