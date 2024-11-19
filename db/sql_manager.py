import json
import math

import pymysql
from pymysql import OperationalError
#
# DB_CONFIG = {
#     "host": "001.pub.mysql.qa.wacai.info",
#     "port": 3307,
#     "user": "qa_conn",
#     "passwd": "qa_conn",
#     "db": "qa_tool",
#     "charset": "utf8"
# }

DB_CONFIG = {
    "host": "rm-bp1pvlqh2itfpe06q6o.mysql.rds.aliyuncs.com",
    "port": 3306,
    "user": "kun",
    "passwd": "root@123456",
    "db": "mitu_toll",
    "charset": "utf8"
}


# DB_CONFIG = {
#     "host": "124.223.168.99",
#     "port": 3307,
#     "user": "root",
#     "passwd": "Chu@123455",
#     "db": "tool_app",
#     "charset": "utf8"
# }


# DB_CONFIG = {
#     "host": "124.223.168.99",
#     "port": 3307,
#     "user": "ckun",
#     "passwd": "Ch@112333",
#     "db": "tool_app",
#     "charset": "utf8"
# }



class SQLManager(str):

    # 初始化实例方法
    def __init__(self, *arg):
        self.conn = None
        self.cursor = None
        self.connect(arg[0])

    def _reCon(self):
        """ MySQLdb.OperationalError异常"""
        # self.con.close()
        while True:
            try:
                self.conn.ping()
                break
            except OperationalError:
                self.conn.ping(True)

    # 连接数据库
    def connect(self, db):
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["passwd"],
            db=db,
            charset=DB_CONFIG["charset"]
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        self._reCon()
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # 查询单条数据
    def get_one(self, sql, args=None):
        self._reCon()
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # 执行单条SQL语句
    def moddify(self, sql, args=None):
        self._reCon()
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 我如果要批量执行多个创建操作，虽然只建立了一次数据库连接但是还是会多次提交，可不可以改成一次连接，
    # 一次提交呢？
    # 可以，只需要用上pymysql的executemany()
    # 方法就可以了。
    # 执行多条SQL语句
    def multi_modify(self, sql, args):
        self._reCon()
        self.cursor.executemany(sql, args)
        self.conn.commit()

    # 创建单条记录的语句
    def create(self, sql, args=None):
        self._reCon()
        self.cursor.execute(sql, args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # 关闭数据库cursor和连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 最后，我们每次操作完数据库之后都要手动关闭，可不可以写成自动关闭的呢？
    # 联想到我们之前学过的文件操作，使用with语句可以实现缩进结束自动关闭文件句柄的例子。
    # 我们来把我们的数据库连接类SQLManager类再优化下，使其支持with语句操作。
    # 进入with语句自动执行
    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# if __name__ == '__main__':
# a = SQLManager('tool_app')
# sql = 'select * from password_info'
# print(a.get_list(sql))
