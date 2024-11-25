import json
import re
from re import split

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
                               user_gender=user_gender) + "".join([f"{i + 1}、{title}" for i, title in
                                                                   enumerate(res_txt_list)])

    log.info("ai_req  ==  " + str(ai_req))

    ai_res = chat_api(ai_req)

    log.info("ai_res  ==  " + str(ai_res))

    # all_present = all(element in str(ai_res) for element in res_txt_list)

    if True:
        return yunshi_response_format(res_txt_list, ai_res['choices'][0]['message']['content'])

    return False


def yunshi_response_format(title_list, text):
    # 构建一个通用正则，匹配目标标题以及其后内容
    result_list = []

    line_content = text.splitlines()
    for line in line_content[:]:
        if count_chinese_characters(line) == 0:
            line_content.remove(line)

    title_indexs = []

    for title in title_list:
        for i, line_new in enumerate(line_content):
            if (title in line_new) & (count_chinese_characters(line_new) < 10):
                title_indexs.append(i)

    for i, t_index in enumerate(title_indexs):
        if i == len(title_indexs) - 1:
            print("last")
            # result_list.append({"title": title_list[i], "res": ''.join(line_content[t_index + 1:])})
        else:
            result_list.append({"title": title_list[i], "res": ''.join(line_content[t_index + 1:title_indexs[i + 1]])})

    return json.dumps(result_list, ensure_ascii=False, indent=2)


def count_chinese_characters(text):
    # 匹配汉字的正则表达式
    pattern = r'[\u4e00-\u9fff]'
    # 使用re.findall找到所有汉字
    chinese_characters = re.findall(pattern, text)
    return len(chinese_characters)


if __name__ == "__main__":

    json_text = '''
    以下是为您生成的一个示例，需要注意的是，周易运势是一种传统的文化观念，其科学性并未得到广泛认可，以下内容仅供娱乐参考。

```json
{
    "命盘分析": {
        "命宫": "根据出生时间推算，命宫显示出此人具有较强的领导能力和决断力，但也可能会有些固执和自我。",
        "五行": "五行中土气较旺，土主信，说明此人较为诚实守信，但也需注意避免过于固执和保守。"
    },
    "婚姻运势": {
        "总体运势": "婚姻运势较为平稳，有机会遇到合适的伴侣，但需要注意沟通和理解，避免因小事产生矛盾。",
        "结婚时间": "在28岁左右有较大的结婚机会。",
        "配偶特点": "配偶可能性格温和，善解人意，能够给予支持和理解。"
    },
    "对方感情特点": {
        "情感表达": "对方在感情中较为细腻，善于表达自己的情感，但也可能会有些敏感。",
        "忠诚度": "对感情较为忠诚，一旦认定对方，会全心全意地付出。",
        "相处方式": "希望在感情中能够得到尊重和理解，喜欢平等的沟通和交流。"
    },
    "桃花运势": {
        "桃花数量": "桃花运势较为不错，一生中会有较多的异性缘。",
        "桃花质量": "桃花质量参差不齐，需要自己仔细辨别，避免陷入不必要的感情纠纷。",
        "桃花出现时间": "在20岁、25岁和30岁左右可能会有比较明显的桃花运势。"
    },
    "财运": {
        "总体财运": "财运较为平稳，通过努力工作可以获得不错的收入，但也需要注意理财规划，避免不必要的开支。",
        "财富来源": "主要的财富来源可能是通过自己的职业发展和投资收益。",
        "财运高峰期": "在35岁左右可能会迎来一个财运的高峰期，需要好好把握机会。"
    },
    "综合运势": {
        "健康": "身体健康状况良好，但需要注意保持良好的生活习惯，避免过度劳累。",
        "事业": "事业发展较为顺利，有机会获得晋升和发展的机会，但需要不断努力提升自己的能力。",
        "人际关系": "人际关系良好，能够得到他人的支持和帮助，但也需要注意处理好与他人的关系，避免产生矛盾和冲突。"
    }
}
```

以上内容仅为根据您的需求生成的示例，不具有实际的预测意义。在现实生活中，我们应该以科学的态度看待事物，通过自己的努力和实际行动来创造美好的未来。'''

    j = json_text.split("```json")[1].split("```")[0]
    data = json.loads(j)
    result = []
    for title, content in data.items():
        result.append({"title": title, "res": str(content)})
    print(result)
