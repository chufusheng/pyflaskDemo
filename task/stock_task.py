import json
import time

from task.stock_scrapy2 import get_stock_data
from db.stock_scrapy_record import *

# 长城汽车
stock_code_list = ["sh601633","sz000980"]


def stock_scrapy_job():
    scrapy_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"任务执行时间: {scrapy_time}")

    for stock_code in stock_code_list:
        res = get_stock_data(stock_code)
        save_stock_scrapy_record(stock_code[2:], scrapy_time, res['price'], res['price_increase'], res['price_percent'])

# if __name__ == '__main__':
#     print(stock_code_list[0][2:])

#
