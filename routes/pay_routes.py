from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, time
import concurrent.futures

from db.pay_info import *
from db.order_info import *
from routes.route_utils import validate_required_fields
from service.aikelai_pay_service import *
import uuid

from service.doubao_ai import chat_api

pay = Blueprint('pay', __name__)


@pay.route('/init', methods=['POST'], strict_slashes=False)  # 首页路由
def pay_init():
    data = request.get_json()
    client_ip = request.remote_addr

    log.info("/pay/init  data = " + str(data))

    # 校验请求参数
    required_fields = ['user_id', 'order_no', 'pay_type']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result is not True:
        return validation_result

    order_info = get_one_order_by_order_no(data['order_no'])

    if order_info is None:
        return "订单不存在"

    try:
        pay_req_no = uuid.uuid4().hex[:20]

        pay_info_id = save_pay_info(user_id=data['user_id'], pay_id=None, pay_req_no=pay_req_no, pay_time=None,
                                    status=0,
                                    order_no=data['order_no'], pay_type=data['pay_type'])

        aikelai_pay_res = aikelai_pay_init(data['pay_type'], pay_req_no, order_info['product_name'],
                                           order_info['amount'] / 100, client_ip)
        if aikelai_pay_res['code'] == 0:
            return "请求支付失败"

        pay_res_data = aikelai_pay_res['data']
        update_pay_info_by_pay_info_id(pay_info_id, pay_id=pay_res_data['trade_no'], pay_time=None, status=1,
                                       pay_url=pay_res_data['payurl'])
    except Exception as e:
        log.error(e)

    return pay_res_data


@pay.route('/callBack', methods=['GET'], strict_slashes=False)  # 首页路由
def pay_call_back():
    data = request.args.to_dict()
    client_ip = request.remote_addr

    log.info(" client_ip = " + client_ip + "/pay/callBack  data = " + str(data))

    if not md5_check(data):
        log.info("签名校验失败")
        return "success"
    if data['trade_status'] == 'TRADE_SUCCESS':
        try:
            pay_info = get_one_pay_info_by_pay_id(data['trade_no'])
            update_pay_info_by_pay_id(pay_id=data['trade_no'], pay_time=datetime.now(), status=2)
            update_order_info(order_no=pay_info['order_no'], pay_time=datetime.now(), status=2)

        except Exception as e:
            log.error("支付成功后表更新异常" + str(e))
    log.info(" with concurrent.futures.ThreadPoolExecutor() as executor:")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(doubao_ai_chat)
        try:
            result = future.result()
            log.info(result)
        except Exception as e:
            log.info("chat更新异常" + str(e))

    return "success"


@pay.route('/test')  # 首页路由
def hello_world():
    return render_template('pay.html')


def doubao_ai_chat(content):
    for i in range(1, 10):
        time.sleep(1)
    return "你好"
    # chat_api(content)

#
# if __name__ == '__main__':
