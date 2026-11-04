# Flask 项目

基于 Flask 3.x 的 RESTful JSON 后端，采用应用工厂（`create_app()`）模式，路由按蓝图拆分在 `app/routes/` 下。

## 环境要求

- Python 3.10+
- 依赖清单见 `requirements.txt`

## 启动步骤

### 1. 创建并激活虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

项目根目录的 `.env` 由 python-dotenv 自动加载，常用变量：

```
FLASK_APP=app
FLASK_DEBUG=true
PORT=4444
SECRET_KEY=改成随机字符串
```

> `DATABASE_URI` 等数据库变量目前未生效，后续接入数据库时再用。

### 4. 启动服务

两种方式任选其一：

```bash
# 方式一：直接运行入口文件
python app.py

# 方式二：使用 Flask 命令行
flask run
```

启动后访问 `http://127.0.0.1:4444`。

在 PyCharm 中也可直接运行 `app.py`（绿色运行按钮）。

## 项目结构

```
flask/
├── app.py              # 启动入口（薄启动器）
├── config.py           # 配置类
├── requirements.txt    # 依赖
├── .env                # 环境变量（不入库）
└── app/                # 应用包
    ├── __init__.py     # 应用工厂 create_app()
    ├── routes/         # 蓝图路由
    ├── models/         # 数据模型
    └── utils/          # 响应封装、错误处理
```

## 接口说明

（TODO：后续补充接口列表与示例）
