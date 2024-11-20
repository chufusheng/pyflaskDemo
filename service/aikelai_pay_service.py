import requests
import hashlib
from config import aikelai_pay

from log_config import CustomLogger as log


def aikelai_pay_init(pay_type, pay_req_no, prduct_name, amount, ip):
    # 请求的URL
    url = "https://pay.aikelaidev.cn/mapi.php"

    type = ""
    if pay_type == 1:
        type = "wxpay"
    elif pay_type == 2:
        type = "alipay"

    # 假设以下是示例数据，你需要根据实际情况替换
    parameters = {"pid": aikelai_pay['appid'], "type": type, "out_trade_no": pay_req_no,
                  "notify_url": aikelai_pay['notify_url'], "return_url": aikelai_pay['return_url'], "name": prduct_name,
                  "device": "jump", "money": amount, "clientip": ip}

    # 计算MD5签名，注意这里要大写
    parameters["sign"] = md5_utils(parameters)
    parameters["sign_type"] = "MD5"

    try:
        # 发送POST请求
        response = requests.post(url, data=parameters)

        # 检查响应状态码
        if response.status_code == 200:
            log.info("aikelai 请求支付结果" + str(response.json()))
            return {"data": response.json(), "code": 1}
        else:
            log.info(f"请求失败：{response.text}")
            return {"data": response.text, "code": 0}
    except requests.exceptions.RequestException as e:
        log.error(f"请求发生异常：{e}")
        return {"code": 0, "error": e}


def md5_utils(parameters):
    sorted_parameters = sorted([(k, v) for k, v in parameters.items() if k not in ["sign", "sign_type"] and v])

    # 步骤2：拼接成URL键值对的格式
    param_str = "&".join([f"{k}={v}" for k, v in sorted_parameters]) + aikelai_pay['key']
    # 构造待签名的字符串

    # 计算MD5签名，注意这里要小写
    sign = hashlib.md5(param_str.encode()).hexdigest().lower()
    return sign


def md5_check(data):
    return data['sign'] == md5_utils(data)


if __name__ == "__main__":
    # aikelai_pay_init(1, "110001", "测试商品", 0.01, "127.0.0.1")

    data = {
        "pid": "1345",
        "trade_no": "2024111917060957594",
        "out_trade_no": "2abbfb2e22304237",
        "type": "wxpay",
        "name": "测试商品001",
        "money": "0.01",
        "trade_status": "TRADE_SUCCESS",
        "sign": "'449d9f084d10b57b56393b53526d68e3'",
        "sign_type": "MD5"
    }
    print(md5_utils(data))
