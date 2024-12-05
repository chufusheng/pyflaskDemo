from flask_apscheduler import APScheduler
from flask import Flask
from routes.ai_test import ai
from routes.order_routes import order
from routes.pay_routes import pay

from flask_cors import *


# 配置类
class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'task.stock_task:stock_scrapy_job',  # 指定任务函数
            # 'args': (1, 2),  # 任务参数
            'trigger': 'cron',  # 使用 cron 表达式触发
            'minute': '*/1',  # 每 10 分钟执行一次
            'hour': '9-11,13-19',  # 只在 9:30 到 11:30 和 13:00 到 15:00 之间执行
            'max_instances': 1  # 限制最多只能有一个实例在执行

        }
    ]


app = Flask(__name__, static_folder='assets')  # 实例化flask
CORS(app, supports_credentials=True)

app.register_blueprint(ai, url_prefix='/ai')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(pay, url_prefix='/pay')

app.config.from_object(Config())  # 为实例化的flask引入配置
# app.config['DEBUG'] = True  # 启用调试模式
#
scheduler = APScheduler()  # 实例化APScheduler
scheduler.init_app(app)  # 把任务列表放进flask
scheduler.start()  # 启动任务列表

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 启动flask
