import json
import re

import requests
from config import doubao_ai
from log_config import CustomLogger as log

# 以下参数视服务不同而不同，一个服务内通常是一致的

Host = "https://ark.cn-beijing.volces.com"
ContentType = "application/json"


def chat_api(content):
    headers = {
        "Content-Type": ContentType,
        "Authorization": "Bearer " + doubao_ai['API_KEY'],
        "X-Security-Token": ""
    }
    data = {
        "model": "ep-20241113163411-hpnvp",
        "messages": [
            {
                "role": "user",
                "content": "{}".format(content)
            }
        ]
    }
    try:
        r = requests.post(Host + '/api/v3/chat/completions', headers=headers, json=data, timeout=200)
        return r.json()
    except Exception as e:
        log.error(e)
        return {"code": 0, "error": e}


def yunshi_req_format(date_type, user_birthday, birthday_hour, user_gender, product_yunshi):
    if date_type == 1:
        date_type_name = "农历"
    else:
        date_type_name = "阳历"

    yunshi = json.loads(product_yunshi)

    req_format = yunshi['req_format']
    res_txt_list = yunshi['res_txt']

    ai_req = req_format.format(user_birthday=user_birthday, birthday_hour=birthday_hour,
                               user_gender=user_gender) + "".join([f"，{item}" for item in res_txt_list])

    log.info("ai_req  ==  " + ai_req)

    ai_res = chat_api(ai_req)

    log.info("ai_res  ==  " + ai_res)

    all_present = all(element in str(ai_res) for element in res_txt_list)

    if all_present:
        return ai_res['choices'][0]['message']['content'].split('---')[1]

    return False


if __name__ == "__main__":
    yunshi_txt = '''{
    "req_format": "阳历 {user_birthday} {birthday_hour}点出生，{user_gender}生，给一个800字周易运势，包含:  ",
    "res_txt": [
        "命盘分析",
        "婚姻运势",
        "桃花运势",
        "财运"
    ]
}'''
    yunshi_req_format(1, '1995-04-01', '8', '男', yunshi_txt)
