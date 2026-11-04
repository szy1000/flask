"""路由包：所有蓝图在这里汇总，统一在 create_app() 里注册。"""


# from flask import Blueprint

# main_bp = Blueprint("main", __name__, url_prefix="/api")
from .blueprint import main_bp
# 必须在蓝图定义之后导入路由模块：import 时 @main_bp.route(...) 装饰器才会执行，
# 路由才会挂到蓝图上。不导入的话蓝图是空的，所有请求都会 404。
from app.routes import main  # noqa: E402
from app.routes import api  # noqa: E402

__all__ = ["main_bp"]
