import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 设置 Chrome 无头模式（不弹出浏览器窗口）
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式，不打开浏览器
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# 配置 WebDriver
# driver_path = './chromedriver'  # WebDriver 的路径
driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver')  # 获取当前脚本所在目录

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def get_stock_data(stock_code):
    # 访问目标页面
    url = "https://data.eastmoney.com/stockdata/{}.html".format(stock_code)
    driver.get(url)

    # 等待页面加载完成，调整为适当的时间
    time.sleep(1)  # 可以根据需要增加等待时间，确保页面加载完成

    # 使用 XPath 获取股票价格
    try:
        price_element = driver.find_element(By.XPATH, '//*[@id="price9"]')
        price_increase_element = driver.find_element(By.XPATH, '//*[@id="km1"]')
        price_percent_element = driver.find_element(By.XPATH, '//*[@id="km2"]')

        price = price_element.text
        price_increase = price_increase_element.text
        price_percent = price_percent_element.text
        #
        # print(f"当前股票价格: {price}")
        # print(f"当前股票趋势: {price_increase}")
        # print(f"当前股票涨幅: {price_percent}")

        return {"price": price, "price_increase": price_increase, "price_percent": price_percent}

    except Exception as e:
        print(f"获取价格失败: {e}")

    # 关闭浏览器
    driver.quit()


# if __name__ == '__main__':
#     print(get_stock_data('601633'))
