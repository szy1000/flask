"""项目入口。

两种启动方式：
  1. 直接运行本文件：python app.py（或 PyCharm 里点绿色运行按钮）
  2. 用 Flask 命令行：flask run（.env 里已经配好 FLASK_APP=app）

注意：这里 import 的 app 是 app/ 包（包优先于同名 .py 文件），
本文件只是一个薄薄的启动器。
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "4444")),
        debug=os.getenv("FLASK_DEBUG", "true").lower() in ("1", "true"),
    )
