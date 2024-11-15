from flask import Blueprint, render_template, request

from db.sql_manager import SQLManager
from config.log_config import setup_logging

logger = setup_logging()

ai = Blueprint('ai', __name__)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@ai.route('/')  # 首页路由
def hello_world():
    return render_template('ai/index.html', name=name, movies=movies)


@ai.route('/upload', methods=['GET', 'POST'])
def upload_test():
    if request.method == 'GET':
        return render_template('ai/photo.html', data='')
    else:
        f = request.files['photo']
        type = request.form.get("l_type")
        print(type)
        txt = image_to_words(f, type)
        return render_template('ai/photo.html', data=txt)


@ai.route('/up_photo', methods=['GET', 'POST'], strict_slashes=False)
def up_photo():
    f = request.files['photo']
    txt = image_to_words(f)
    return render_template('ai/photo.html', data=txt)


@ai.route('/ai_chat', methods=['GET', 'POST'], strict_slashes=False)
def ai_chat():
    oldRes = request.args.get("oldRes")
    msg = request.args.get("msg")
    res = voice_chat(oldRes, msg)
    return res


@ai.route('/ai_chat_index', methods=['GET', 'POST'], strict_slashes=False)
def ai_chat_index():
    return render_template('ai/chat.html')


def storing_statistical():
    db = SQLManager("3dthing")

    page_count = 10000
    sql = "select id,file_size from things_files order by id desc limit {0}, {1};"
    mb_count = 0
    kb_count = 0
    for page in range(1, 51):
        print(page)
        list = db.get_list(sql.format((page - 1) * page_count, page_count))
        for i in list:
            try:
                data = str(i['file_size']).split(' ')
                num = int(data[0])
                unit = data[1]
                if unit.__contains__('mb'):
                    mb_count = mb_count + num
                if unit.__contains__('kb'):
                    kb_count = kb_count + num
            except Exception as e:
                print("-----")
                print(i["id"])

    print(mb_count * 1024 + kb_count)


@ai.route('/payres', methods=['GET', 'POST'], strict_slashes=False)  # 首页路由
def payres():
    data = request.get_json()
    logger.info(data)
    logger.info("@ai.route('/payres', methods=['GET', 'POST'], strict_slashes=False)  # 首页路由")
    print(data)
    return "success"


if __name__ == '__main__':
    storing_statistical()
