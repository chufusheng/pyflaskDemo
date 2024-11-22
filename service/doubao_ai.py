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
    pattern = re.compile(
        r'(.*?)\s*(1\.|2\.|3\.|4\.|5\.|6\.)?\s*[*\*]?(\S+?)\s*[:：]\n?([\s\S]*?)(?=\s*1\.|\s*2\.|\s*3\.|\s*4\.|\s*5\.|\s*6\.|$)',
        re.MULTILINE)

    # 初始化结果列表
    result_list = []

    # 遍历匹配到的结果
    for match in pattern.findall(text):
        section_title = match[2].strip()
        section_content = match[3].strip()

        # 检查标题是否在目标标题列表中
        for target_title in title_list:
            if target_title in section_title:
                result_list.append({
                    "title": target_title,
                    "res": section_content
                })
                break

    # 返回 JSON 格式结果
    return json.dumps(result_list, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    titile = ['命盘分析', '婚姻运势', '对方感情特点', '桃花运势', '财运', '综合运势']
    #     yunshi_txt = '''{
    #     "req_format": "阳历 {user_birthday} {birthday_hour}点出生，{user_gender}生，给一个800字周易运势，包含:  ",
    #     "res_txt": [
    #         "命盘分析",
    #         "婚姻运势",
    #         "桃花运势",
    #         "财运"
    #     ]
    # }'''
    #     yunshi_req_format(1, '1995-04-01', '8', '男', yunshi_txt)
    #
    txt = {'choices': [{'finish_reason': 'stop', 'index': 0, 'logprobs': None, 'message': {
        'content': '作为AI语言模型，我需要提醒您，周易运势是一种传统文化的解读方式，其科学性并未得到广泛认可。以下内容仅供参考，您可以抱着理性和客观的态度看待。\n\n根据您提供的出生时间2018年3月9日12点，以下是一个简单的周易运势分析：\n\n命盘分析\n    - 该男生出生于戊戌年乙卯月庚子日壬午时。庚金生于卯月，木旺金囚，日主庚金较弱。年柱戊戌土厚，可生助庚金，但卯戌合，土的力量有所减弱。月柱乙卯木旺，对庚金有一定克制作用。日支子水为庚金的伤官，时柱壬午，午火为正官，壬水为食神。总体来说，命盘中五行力量较为复杂，需要综合分析各个因素的相互作用。\n\n2婚姻运势\n    - 从命盘来看，日主庚金的配偶星为乙木。乙卯月出生，乙木当令，配偶星较强。这可能意味着在婚姻中，对方会比较有个性和主见。婚姻宫为子水，子水为伤官，可能会对婚姻关系产生一定的影响，需要注意沟通和理解，避免因个性问题而产生矛盾。\n    - 该男生在选择伴侣时，可能会倾向于聪明、有才华的女性。在婚姻中，需要学会尊重对方的意见，共同经营好家庭。中年时期可能会面临一些婚姻上的挑战，需要双方共同努力克服。\n\n3. **对方感情特点**：\n    - 由于配偶星为乙木，对方可能具有温柔、善良、有艺术气质的特点。同时，乙木的人可能比较感性，注重情感交流。在感情中，对方可能会希望得到更多的关心和呵护，同时也会给予对方相应的回应。\n\n*桃花运势9876789**：\n    - 庚子日出生的人，桃花较为旺盛。在年轻时，可能会有较多的异性缘。但需要注意把握好分寸，避免因桃花问题而影响到自己的感情和生活。\n    - 逢兔年、马年、鼠年等年份，桃花运势可能会较为明显。在这些年份中，需要注意自己的言行举止，避免给人留下不好的印象。\n\n5. **财运**：\n    - 命盘中土为印星，可生助日主，有一定的旺财作用。但木旺克土，印星的力量受到一定的制约。财运方面，需要通过自己的努力和智慧去获取财富，避免盲目投资和冒险。\n    - 中年时期财运可能会有所好转，但需要注意理财规划，避免浪费和不必要的开支。\n\n6. **综合运势**：\n    - 该男生的命盘五行力量较为复杂，需要在生活中不断调整自己的心态和行为方式，以适应不同的环境和挑战。\n    - 年轻时可能会面临一些挫折和困难，但通过自己的努力和坚持，能够逐渐克服。中年时期运势会有所好转，事业和财运都有一定的发展机会。但需要注意保持谦虚和谨慎，避免因骄傲自满而导致失败。\n    - 在健康方面，需要注意肝胆、肠胃等方面的问题，保持良好的生活习惯和饮食习惯。\n\n需要注意的是，以上分析仅基于周易命理学的理论，其准确性和科学性并未得到广泛认可。人的命运是由多种因素共同决定的，包括个人的努力、环境、教育等。因此，我们应该以积极的态度面对生活，通过自己的努力去创造美好的未来。',
        'role': 'assistant'}}], 'created': 1732250147, 'id': '0217322501068436c3e287e1f5e2707e686ac6c758aa79d5a8c22',
           'model': 'doubao-pro-128k-240628', 'object': 'chat.completion',
           'usage': {'completion_tokens': 773, 'prompt_tokens': 62, 'total_tokens': 835}}

    yunshi_response_format(titile, txt['choices'][0]['message']['content'])
