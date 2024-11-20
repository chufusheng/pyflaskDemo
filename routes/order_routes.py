from flask import Blueprint, request, jsonify

from log_config import CustomLogger as log
from db.order_info import *
from db.prduct_info import *
from routes.route_utils import validate_required_fields

import uuid

order = Blueprint('order', __name__)


@order.route('/init', methods=['POST'], strict_slashes=False)  # 首页路由
def order_init():
    data = request.get_json()
    client_ip = request.remote_addr

    log.info("/order/init  data = " + str(data))

    # 校验请求参数
    required_fields = ['user_id', 'user_name', 'user_birthday', 'birthday_hour', 'user_gender', 'product_key']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result is not True:
        return validation_result

    product_info = get_one_product_info_by_product_key(data['product_key'])

    if not product_info:
        return jsonify({"error": f"未查询到{data['product_key']} 的产品信息"}), 400

    order_no = uuid.uuid4().hex[:16]

    save_order_info(user_id=data['user_id'], order_no=order_no, amount=product_info['amount'],
                    status=1, user_name=data['user_name'], user_birthday=data['user_birthday'],
                    birthday_hour=data['birthday_hour'], user_gender=data['user_gender'],
                    product_id=product_info['product_key'], product_name=product_info['product_name'], yunshi_status=1
                    , pay_time=None, yunshi=None, ip=client_ip)

    return "success"


@order.route('/list', methods=['GET'], strict_slashes=False)  # 首页路由
def order_list():
    data = request.args.to_dict()
    client_ip = request.remote_addr

    log.info(" client_ip = " + client_ip + "/order/list  data = " + str(data))

    # 校验请求参数
    required_fields = ['user_id']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result is not True:
        return validation_result

    order_info = get_order_list_by_user_id(data['user_id'])

    log.info(" order_info = " + str(order_info))

    return jsonify(order_info)


@order.route('/info', methods=['GET'], strict_slashes=False)  # 首页路由
def order_info():
    data = request.args.to_dict()
    client_ip = request.remote_addr

    log.info(" client_ip = " + client_ip + "/order/info  data = " + str(data))

    # 校验请求参数
    required_fields = ['order_no']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result is not True:
        return validation_result

    order_info = get_one_order_by_order_no(data['order_no'])

    log.info(" order_info = " + str(order_info))

    return jsonify(order_info)


#
if __name__ == '__main__':
    uuid_16bit = uuid.uuid4().hex[:16]
    print(uuid_16bit)
