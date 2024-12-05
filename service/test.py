import json
import re

text = '''


# 《周易运势分析 - 2018 年 3 月 9 日 12 时出生的男生》

根据您提供的出生时间，2018 年 3 月 9 日 12 时，男生，我们可以通过周易的方法来分析他的运势。

## 一、命盘分析
首先，我们需要确定命盘中的天干地支。2018 年为戊戌年，3 月为乙卯月，9 日为庚子日，12 时为午时，对应的天干地支为甲午。根据这些信息，我们可以构建出一个初步的命盘。

在这个命盘中，庚金生于卯月，木旺金囚。日主庚金偏弱，需要土金来生扶。年柱戊戌土厚，可以起到生扶日主的作用，但戊土被乙木所克，力量有所减弱。月柱乙卯木旺，对日主庚金形成一定的克制。日柱庚子，子水泄庚金之气，也对日主不利。时柱甲午，甲木生火，午火克金，对日主也有一定的压力。综合来看，日主庚金偏弱，喜土金，忌木火水。

## 二、婚姻运势
从命盘来看，这位男生的婚姻运势较为平稳。他的配偶星为乙木，乙木在月柱上透出，说明他的配偶可能会在他年轻时出现。配偶星乙木为正财，代表着他的配偶性格温和，善良，懂得持家理财。在婚姻生活中，他们会相互关心，相互支持，共同经营好家庭。

然而，由于命盘中木旺克金，可能会在婚姻中遇到一些小的摩擦和矛盾。特别是在夫妻沟通方面，需要多加注意，避免因为一些小事而产生误会和争吵。建议他在婚姻中要多一些包容和理解，尊重配偶的意见和想法，这样才能保持婚姻的幸福美满。

## 三、对方感情特点
他的配偶在感情上比较细腻，注重情感的交流和沟通。她会关心他的生活和工作，给予他支持和鼓励。同时，她也希望得到他的关注和回应，希望在感情中能够感受到彼此的爱意和温暖。

配偶的性格可能会比较柔顺，但也有自己的主见和想法。在面对问题时，她会冷静地分析和处理，不会轻易地发脾气或做出冲动的决定。她会尊重他的选择和决定，同时也会提出自己的建议和意见，帮助他更好地解决问题。

## 四、桃花运势
在桃花运势方面，这位男生的桃花运势较为一般。由于命盘中木旺克金，对他的感情运势有一定的影响。他可能不会有太多的桃花机会，但是一旦遇到合适的人，就会有比较稳定的感情发展。

在寻找另一半时，他需要注意不要过于挑剔和追求完美，要学会发现对方的优点和长处。同时，他也需要注意自己的言行举止，保持良好的形象和气质，这样才能吸引到更多的异性关注。

## 五、财运
从命盘来看，这位男生的财运还算不错。年柱戊戌土为正印，代表着长辈的帮助和支持，也代表着他有一定的福气和财运。月柱乙卯木为正财，说明他有一定的赚钱能力和理财能力，能够通过自己的努力获得一定的财富。

然而，由于命盘中木旺克金，他在财运方面也会遇到一些挑战和压力。特别是在投资和理财方面，需要谨慎对待，避免因为盲目投资而导致财产损失。建议他在理财方面要多学习一些专业知识，提高自己的理财能力和风险意识。同时，他也可以借助长辈的经验和智慧，帮助自己更好地规划财务。

## 六、综合运势
综合来看，这位男生的运势总体上还算不错。在婚姻方面，他需要多一些包容和理解，才能保持婚姻的幸福美满。在桃花运势方面，他需要注意自己的言行举止，提高自己的吸引力。在财运方面，他需要谨慎对待投资和理财，避免财产损失。

当然，周易运势分析只是一种参考，不能完全决定一个人的命运。一个人的命运是由多种因素共同决定的，包括个人的努力、环境的影响、机遇的把握等等。希望这位男生能够在未来的生活中，积极面对挑战，努力奋斗，创造出属于自己的美好未来。


'''

json_res = {'choices': [{'finish_reason': 'stop', 'index': 0, 'logprobs': None, 'message': {
    'content': '需要注意的是，周易算命是一种传统文化的表现形式，其结果并没有科学依据，不能被视为对个人命运的准确预测。以下内容仅供娱乐：\n\n---\n\n# 《周易算命结果》\n\n## 一、命盘分析\n根据您提供的出生时间，2018年3月9日12点，男生，对应的八字为：戊戌年乙卯月庚子日壬午时。\n\n庚金生于卯月，木旺金囚，日主庚金不得月令之助。年柱戊戌土生金，月干乙木耗金，日支子水泄金，时干壬水泄金，时支午火克金。综合来看，日主庚金偏弱，喜土金帮扶，忌木水火。\n\n## 二、婚姻运势\n在婚姻方面，命主的配偶可能会是一个聪明、机智、有才华的人。对方可能具有较强的沟通能力和表达能力，能够与命主进行良好的交流和互动。然而，命主在婚姻中需要注意避免过于强势和固执，要学会尊重和理解对方的想法和感受，这样才能保持婚姻的和谐与稳定。\n\n从流年运势来看，命主在适婚年龄时，可能会遇到一些感情上的波折和挑战。例如，在某些年份可能会出现争吵、矛盾等情况，但只要双方能够相互包容、理解，共同努力克服困难，还是能够顺利度过这些难关，走向幸福的婚姻生活。\n\n## 三、对方感情特点\n命主的配偶在感情方面可能会比较细腻、敏感，注重情感的交流和沟通。对方可能会比较在意命主的感受和需求，会尽力为命主创造一个温馨、和谐的家庭氛围。同时，对方也可能会有一些情绪化的表现，需要命主在相处过程中给予更多的关心和安慰。\n\n## 四、桃花运势\n命主的桃花运势较为一般。在年轻时，可能会有一些短暂的桃花出现，但大多不是正缘。命主在感情方面需要保持清醒的头脑，不要被一时的冲动所迷惑，要学会分辨真正适合自己的人。在中年以后，命主的桃花运势会有所好转，可能会遇到一个真正与自己相互欣赏、相互扶持的人。\n\n## 五、财运\n命主的财运总体来说还算不错。由于日主庚金偏弱，喜土金帮扶，因此命主在从事与土、金相关的行业时，可能会有较好的财运。例如，房地产、建筑、金属加工等行业。此外，命主在投资理财方面也需要谨慎一些，避免盲目跟风和冒险投资，以免造成不必要的损失。\n\n从流年运势来看，命主在青年时期财运可能会比较起伏不定，需要通过自己的努力和奋斗才能逐渐积累财富。在中年以后，命主的财运会逐渐稳定下来，并且有机会获得较大的财富收益。\n\n## 六、综合运势\n总体来说，命主的运势较为平稳。在事业方面，命主需要不断努力学习和提升自己的能力，才能在竞争激烈的社会中脱颖而出。在健康方面，命主需要注意呼吸系统和消化系统的问题，平时要多注意休息和饮食健康。在人际关系方面，命主需要学会与人相处的技巧，保持良好的人际关系，这样才能为自己的事业和生活带来更多的帮助和支持。\n\n## 七、星座内容\n2018年3月9日出生的人是双鱼座。双鱼座的人通常具有丰富的想象力和创造力，他们善良、敏感、富有同情心，对艺术和音乐有着浓厚的兴趣。双鱼座的人在人际关系中往往表现得比较温和、友善，容易与人相处。然而，双鱼座的人有时也会显得过于情绪化和优柔寡断，需要学会控制自己的情绪和做出果断的决策。\n\n---\n\n以上内容仅供娱乐，希望您不要过分迷信。命运是掌握在自己手中的，通过自己的努力和奋斗，才能创造出美好的未来。',
    'role': 'assistant'}}], 'created': 1732527028, 'id': '02173252698516982365d4a5b5274956b3afa8f956d92c4822444',
            'model': 'doubao-pro-128k-240628', 'object': 'chat.completion',
            'usage': {'completion_tokens': 846, 'prompt_tokens': 79, 'total_tokens': 925}}


def extract_content_by_title(title_list, text):

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


if __name__ == '__main__':
    t_list = ['命盘分析', '婚姻运势', '对方感情特点', '桃花运势', '财运', '综合运势', '星座内容']
    # print(extract_content_by_title(['命盘分析', '婚姻运势', '桃花运势', '财运', '综合运势'], text))
    data_res = []

    res = json_res['choices'][0]['message']['content']

    print(extract_content_by_title(t_list,res))

    # line_content = res.splitlines()
    # for line in line_content[:]:
    #     if count_chinese_characters(line) == 0:
    #         line_content.remove(line)
    #
    # title_indexs = []
    #
    # for title in t_list:
    #     for i, line_new in enumerate(line_content):
    #         if (title in line_new) & (count_chinese_characters(line_new) < 10):
    #             title_indexs.append(i)
    #
    # for i, t_index in enumerate(title_indexs):
    #     if i == len(title_indexs) - 1:
    #         data_res.append({"title": t_list[i], "res": ''.join(line_content[t_index + 1:])})
    #     else:
    #         data_res.append({"title": t_list[i], "res": ''.join(line_content[t_index + 1:title_indexs[i + 1]])})
    #
    # print(data_res)
    #
