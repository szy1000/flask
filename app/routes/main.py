"""演示路由（JSON）：路径参数、查询参数的用法示例。"""

from flask import request

from app.utils.responses import fail, ok
from .blueprint import main_bp
from app.forms.book import SearchForm


@main_bp.route("/")
def index():
    """接口索引：列出所有可用接口。"""
    return ok(data={
        "name": "Flask RESTful 示例项目",
        "endpoints": {
            "GET /about/<name>": "路径参数示例",
            "GET /search?q=关键词": "查询参数示例（也支持 /search/<关键词>）",
            "GET /api/ping": "健康检查",
            "GET/POST /api/hello": "参数获取示例",
            "GET /api/zhejiang": "浙江培训网数据查询（支持 ?date= 和 ?zj=）",
        },
    })


@main_bp.route("/about/<name>")
def about(name):
    """路径参数示例：URL 里的 <name> 自动作为参数传入。"""
    return ok(data={"name": name})


@main_bp.route("/book/search")
@main_bp.route("/book/search/<keyword>")
def search():
    """查询参数示例：/search?q=关键词 或 /search/关键词，参数缺失返回 400。"""
    # kw = request.args.get("q", "")
    form = SearchForm(request.args)
    if form.validate():
        print(f"{form.keywords.data}")
        return ok(data={"keyword": form.keywords.data, "page": form.page.data})
    return fail(message=form.errors, code=400)
