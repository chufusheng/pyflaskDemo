import requests


def get_stock_data(code):
    # 模拟 API 请求的 URL 和请求头
    api_url = 'http://qt.gtimg.cn/q={}'  # 假设的 API 地址
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    # 发起 GET 请求
    response = requests.get(api_url.format(code), headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.text  # 假设返回的是 JSON 数据
        stock_data = data.split('~~')[1].split('~')
        return {"price": stock_data[5].split('/')[0], "price_increase": str(stock_data[1]),
                "price_percent": str(stock_data[2]) + "%"}
    else:
        print(f"请求失败，状态码：{response.status_code}")


if __name__ == '__main__':
    print(get_stock_data('601633'))
