from flask import Flask, jsonify, request


app = Flask(__name__)


def validate_required_fields(data, required_fields):
    """
    校验给定数据中是否包含所有必需的字段

    :param data: 接收到的包含请求参数的字典
    :param required_fields: 必需字段组成的列表
    :return: 如果所有必需字段都存在则返回True，否则返回False并通过Flask的jsonify返回错误信息和400状态码
    """
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is missing"}), 400
    return True