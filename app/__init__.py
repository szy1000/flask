"""Flask 应用包。

采用「应用工厂」模式：create_app() 负责创建和配置应用实例，
路由拆成蓝图放在 app/routes/ 目录下，错误处理放在 app/errors.py。
"""

from flask import Flask
from config import Config


def create_app(config_class=Config):
    """创建并初始化 Flask 应用。"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config_class)
    # 让 jsonify 返回中文时不转义成 \uXXXX
    app.json.ensure_ascii = False

    from app.models.book import db
    from app.models.actual_data import ActualData
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # print(app.config["SQLALCHEMY_DATABASE_URI"])
    # 注册路由蓝图
    register_blueprints(app)




    return app


def register_blueprints(app):

    # 注册全局错误处理
    from app.utils.errors import register_error_handlers
    register_error_handlers(app)

    from app.routes import main_bp

    app.register_blueprint(main_bp)
    # app.register_blueprint(api_bp)
