# from flask_apscheduler import APScheduler
from flask import Flask
from routes.ai_test import ai
from flask_cors import *

app = Flask(__name__)  # 实例化flask
CORS(app, supports_credentials=True)

app.register_blueprint(ai, url_prefix='/ai')

#
# scheduler = APScheduler()  # 实例化APScheduler
# scheduler.init_app(app)  # 把任务列表放进flask
# scheduler.start()  # 启动任务列表

if __name__ == '__main__':
    # scheduler = APScheduler()  # 实例化APScheduler
    # scheduler.init_app(app)  # 把任务列表放进flask
    # scheduler.start()  # 启动任务列表
    app.run(host='0.0.0.0', port=5000)  # 启动flask
