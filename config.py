"""项目配置。

python-dotenv 会把项目根目录 .env 文件里的变量加载进环境变量，
所以 SECRET_KEY、PORT 等都可以在 .env 里改，不用动代码。
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """默认配置（开发环境够用）。"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-请改成随机字符串")
