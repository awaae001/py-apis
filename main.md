# Steam爬虫API项目

## 项目简介

这是一个基于 Flask 构建的 API 项目，旨在从 Steam 商店页面抓取并返回游戏、捆绑包、折扣、价格等相关信息。用户可以通过提供 Steam 游戏或捆绑包的 ID 来获取详细的价格信息以及包含的游戏列表。该项目使用 `requests` 和 `BeautifulSoup` 来抓取网页内容并解析 HTML 页面。

## 项目结构

```
├── main.py              # Flask API 应用入口文件
├── routes/              # API 路由文件夹
│   ├── steam.py         # 处理 Steam 游戏相关的路由
│   ├── pack.py          # 处理 Steam 捆绑包相关的路由
│   └── ...              # 其他可能的路由文件
├── modules/             # 功能模块文件夹
│   ├── steam.py         # 获取 Steam 游戏信息的模块
│   ├── pack.py          # 获取 Steam 捆绑包信息的模块
│   └── ...              # 其他功能模块
├── templates/           # 存放可能的 HTML 模板文件（如果需要）
├── .venv/               # Python 虚拟环境文件夹
├── requirements.txt     # 项目依赖列表
└── README.md            # 项目描述文件
```

### 文件功能描述：

- **main.py**：应用程序的入口文件，设置了 Flask 的基础 API 配置，包含了各个路由的注册。
- **routes/**：存放 API 路由的文件夹，每个文件对应不同的 API 功能，例如游戏信息、捆绑包信息等。
- **modules/**：包含各个功能模块，负责具体的爬虫逻辑，数据解析和处理。每个模块会使用 `requests` 获取页面，使用 `BeautifulSoup` 解析页面，提取所需信息。
- **.venv/**：虚拟环境文件夹，包含项目的所有 Python 包依赖。
- **requirements.txt**：记录项目的依赖包，以便他人能够通过 `pip install -r requirements.txt` 安装所需依赖。

## 主要功能

1. **Steam 游戏信息抓取**
   - API 路由：`/api/steam/game?id=<game_id>`
   - 功能：根据传入的游戏 ID 获取该游戏的详细信息，包括价格、折扣信息、语言支持等。

2. **Steam 捆绑包信息抓取**
   - API 路由：`/api/steam/pack?id=<bundle_id>`
   - 功能：根据传入的捆绑包 ID 获取该捆绑包的详细信息，包括捆绑包的总价、折扣、包含的游戏及其 ID。

## 使用说明

### 安装依赖

1. 克隆该项目到本地：
   ```bash
   git clone <项目仓库地址>
   cd <项目目录>
   ```

2. 创建并激活虚拟环境：
   ```bash
   python3 -m venv .venv  # 创建虚拟环境
   source .venv/bin/activate  # 激活虚拟环境
   ```

3. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 运行项目

1. 在开发模式下运行 Flask 应用：
   ```bash
   python main.py
   ```

2. 在生产模式下，使用 Gunicorn 运行 Flask 应用：
   ```bash
   gunicorn -w 4 main:app
   ```

3. 访问 API：
   - 获取 Steam 游戏信息：`http://127.0.0.1:5000/api/steam/game?id=2704110`
   - 获取 Steam 捆绑包信息：`http://127.0.0.1:5000/api/steam/pack?id=43192`

### API 示例

1. **获取游戏信息**
   - 请求 URL：`/api/steam/game?id=2704110`
   - 返回 JSON 示例：
     ```json
     {
       "game_id": 2704110,
       "name": "Aliya",
       "price": "¥ 350",
       "discount": "5%",
       "languages": ["简体中文", "英语"]
     }
     ```

2. **获取捆绑包信息**
   - 请求 URL：`/api/steam/pack?id=43192`
   - 返回 JSON 示例：
     ```json
     {
       "bundle_id": 43192,
       "name": "Aliya 音画整合包",
       "price": "¥ 555",
       "discount": "5%",
       "included_games": [2704110, 3041090]
     }
     ```

## 依赖项

- **Flask**：Web 框架，用于处理 HTTP 请求和响应。
- **requests**：用于从 Steam 获取页面内容。
- **beautifulsoup4**：用于解析 HTML 页面并提取数据。
- **gunicorn**：生产环境服务器，用于运行 Flask 应用。
- **flask-cors**：用于处理跨域请求（如需要）。

## 注意事项

- 请确保您的 Python 环境中安装了所有必要的包，最好使用虚拟环境进行隔离。
- 由于爬虫程序涉及从外部网站抓取数据，请确保遵守 Steam 的使用条款和隐私政策，避免对网站产生过大的压力。

这个文件描述了项目的结构、功能、使用方法以及如何安装和运行。开发者可以根据这个描述了解项目的各个部分，并根据需要进行进一步的开发或部署。如果是 AI 需要理解这个项目的工作原理，它可以帮助理解项目的核心功能和组件。