"""全局错误处理：任何错误都返回统一格式的 JSON，而不是 HTML 页面。"""

from werkzeug.exceptions import HTTPException

from app.utils.responses import fail

# 常见 HTTP 错误码对应的中文提示
DEFAULT_MESSAGES = {
    400: "请求参数错误",
    404: "接口不存在",
    405: "请求方法不允许",
    500: "服务器内部错误",
}


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """404、405、400 等所有 HTTP 错误都走这里。"""
        code = e.code or 500
        message = DEFAULT_MESSAGES.get(code, e.description)
        return fail(message=message, code=code)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """没被上面接住的未知异常，统一按 500 处理，避免把堆栈直接抛给前端。"""
        app.logger.exception(e)
        # 异常细节只在 debug 模式下返回，生产环境不泄露内部信息
        message = f"服务器内部错误: {e}" if app.debug else "服务器内部错误"
        return fail(message=message, code=500)
