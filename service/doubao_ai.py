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
        return yunshi_res_format(r.json())
    except Exception as e:
        log.error(e)
        return {"code": 0, "error": e}

def yunshi_res_format(data):
    # todo
    return data



def yunshi_req_format(date_type, birthday, hour, sex):
    if date_type == 1:
        date_type_name = "农历"
    else:
        date_type_name = "阳历"
    if sex == 1:
        sex_CN = "男"
    else:
        sex_CN = "女"
    return "[" + date_type_name + " " + birthday + " " + hour + "点出生 " + sex_CN + "] 给一个800字周易运势，包含：1、婚姻运势2、对方感情特点 3、桃花运势4、财运"


if __name__ == "__main__":
    # result = chat_api("阳历 1995-5-9 23点出生，女生，给一个800字周易运势，包含：1、婚姻运势2、对方感情特点 3、桃花运势4、财运")
    result = chat_api("你好")
    print(result)

    print(result.get("choices")[0].get("message").get("content"))
    print(
        "阳历 {birthday} {birthday_hour}点出生，{gender}生，给一个800字周易运势，包含：1、婚姻运势2、对方感情特点 3、桃花运势4、财运")
