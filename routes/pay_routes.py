from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, request, jsonify, render_template, after_this_request
import concurrent.futures
import time
from db.pay_info import *
from db.order_info import *
from db.prduct_info import *
from routes.route_utils import validate_required_fields
from service.aikelai_pay_service import *
import uuid

from service.doubao_ai import chat_api, yunshi_req_format

pay = Blueprint('pay', __name__)

executor = ThreadPoolExecutor(2)


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
            executor.submit(doubao_ai_chat, pay_info['order_no'])

        except Exception as e:
            log.error("支付成功后表更新异常" + str(e))
            return 'success'

    return "success"


def doubao_ai_chat(order_no):

    log.info("chat_ai start  order_no==    " + order_no)

    order_info = get_one_order_by_order_no(order_no)
    product_info = get_one_product_info_by_product_key(order_info['product_id'])

    user_birthday = order_info['user_birthday']
    birthday_hour = order_info['birthday_hour']
    user_gender = order_info['user_gender']

    res = yunshi_req_format(2, user_birthday, birthday_hour, user_gender, product_info['product_yunshi'])
    log.info("chat_ai res=   " + str(res))

    if res:
        update_order_info(order_no=order_no, yunshi=str(res), yunshi_status=3)


@pay.route('/test')  # 首页路由
def hello_world():
    return render_template('pay.html')


#
if __name__ == '__main__':
    doubao_ai_chat('2abbfb2e22304237')
