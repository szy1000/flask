"""API 路由（JSON）。

蓝图带 url_prefix="/api"，所以这里写的路由实际路径是 /api/xxx。
所有返回值都用 app/responses.py 里的 ok() / fail() 封装。
"""

from requests import RequestException, post

from flask import request
from .blueprint import main_bp

from app.utils.responses import fail, ok

# api_bp = Blueprint("api", __name__, url_prefix="/api")


@main_bp.route("/ping")
def ping():
    """健康检查接口。"""
    return ok(message="pong")


@main_bp.route("/hello", methods=["GET", "POST"])
def hello():
    """演示两种取参数的方式：GET 用查询参数 ?name=，POST 用 JSON 请求体。"""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "")
    else:
        name = request.args.get("name", "")
    return ok(data={"greeting": f"你好，{name or '陌生人'}！"})


@main_bp.route("/zhejiang")
def zhejiang():
    """查询浙江培训网的供需日数据（从原 app.py 迁移，加了超时和错误处理）。

    可选查询参数：?date=2026-10-26&zj=0200003
    """
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "ClientTag": "OUTNET_BROWSE",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "CurrentRoute": "/pxf-settlement-outnetpub-phbzj/columnHomeLeftMenuNew",
        "Origin": "https://zjpx.com.cn",
        "Referer": "https://zjpx.com.cn/pxf-settlement-outnetpub-phbzj/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Secure-Sign-Reponse": "true",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
        "X-Token": "undefined",
        "sec-ch-ua": '"Google Chrome";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    cookies = {
        "BIGipServerxyddljy_newmain_20080": "1822890412.28750.0000",
        "Gray-Tag": "62616f6e656e776b64",
        "ClientTag": "OUTNET_BROWSE",
        "X-Token": "undefined",
        "BIGipServerxyddljy_newmain_80": "18881196.20480.0000",
        "Admin-Token": "977904f26c1e19b339452b6c3be7e667828230f404365206a2802aad7ad3617778d7f95cf58203a4b7e1746ba16509a857a25efeba972d4d78e499699fa3bb81.448261b6d36081bfd7a785fe48020f41301a0aac",
        "X-Ticket": "977904f26c1e19b339452b6c3be7e667828230f404365206a2802aad7ad3617778d7f95cf58203a4b7e1746ba16509a857a25efeba972d4d78e499699fa3bb81.448261b6d36081bfd7a785fe48020f41301a0aac",
        "CurrentRoute": "/dashboard",
    }

    payload = {
        "pageInfo": {
            "pageSize": 10,
            "pageNum": 1,
        },
        "data": {
            "queryDate": request.args.get("date", "2026-10-26"),
            "zjNumber": request.args.get("zj", "0200003"),
            "measType": None,
        },
    }

    try:
        resp = post(
            "https://zjpx.com.cn/px-settlement-infpubquery-phbzj/supplyAndDemand/dailyLoad",
            headers=headers,
            cookies=cookies,
            json=payload,
            timeout=10,
        )
        resp.raise_for_status()
        return ok(data=resp.json())
    except (RequestException, ValueError) as exc:
        # 外部接口挂了/超时/返回非 JSON 时，返回 502 而不是 500
        return fail(message=f"请求外部接口失败: {exc}", code=502)
