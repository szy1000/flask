"""统一响应封装。

所有接口的返回体格式固定为：
    {"code": 200, "message": "success", "data": ...}

code 与 HTTP 状态码保持一致：200 表示成功，4xx/5xx 表示失败。
data 成功时放业务数据，失败时为 null。
"""

from flask import jsonify


def ok(data=None, message="success", code=200):
    """成功响应：ok(data=...) -> {"code": 200, "message": "success", "data": ...}"""
    return jsonify({"code": code, "message": message, "data": data}), code


def fail(message="error", code=400, http_status=None):
    """失败响应：body 里的 code 是错误码，默认 HTTP 状态码与其一致。"""
    return jsonify({"code": code, "message": message, "data": None}), http_status or code
