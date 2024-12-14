# Steam爬虫API项目

## 项目简介

这是一个基于 Flask 构建的 API 项目，旨在从 Steam 商店页面抓取并返回游戏、捆绑包、折扣、价格等相关信息。用户可以通过提供 Steam 游戏或捆绑包的 ID 来获取详细的价格信息以及包含的游戏列表。该项目使用 `requests` 和 `BeautifulSoup` 来抓取网页内容并解析 HTML 页面。

## 项目结构

```
├── README.md                    #  项目介绍         
├── main.py                      #  项目的入口文件
├── modules                      #  模块文件夹
│   ├── github                   #  GitHub API 模块
│   │   ├── __init__.py
│   │   ├── github_rep.py        #  GitHub 仓库信息
│   │   └── github_user.py       #  GitHub 用户信息
│   └── steam                    #  Steam 商店页面解析模块
│       ├── __init__.py          
│       ├── steam_pack.py        #  Steam 捆绑包信息
│       └── steam_utils.py       #  Steam 通用信息解析
├── routes                       #  路由文件夹
│   ├── __init__.py
│   ├── github.py                #  GitHub 路由
│   └── steam.py                 #  Steam 路由
└── temp                         #  临时文件
```

### 文件功能描述：

- **main.py**：应用程序的入口文件，设置了 Flask 的基础 API 配置，包含了各个路由的注册。
- **routes/**：存放 API 路由的文件夹，每个文件对应不同的 API 功能，例如游戏信息、捆绑包信息等。
- **modules/**：包含各个功能模块，负责具体的爬虫逻辑，数据解析和处理。每个模块会使用 `requests` 获取页面，使用 `BeautifulSoup` 解析页面，提取所需信息。
- **requirements.txt**：记录项目的依赖包，以便他人能够通过 `pip install -r requirements.txt` 安装所需依赖。

## 主要功能

1. **Steam 游戏信息抓取**
   - API 路由：`/api/steam/game?id=<game_id>`
   - 功能：根据传入的游戏 ID 获取该游戏的详细信息，包括价格、折扣信息、语言支持等。

2. **Steam 捆绑包信息抓取**
   - API 路由：`/api/steam/pack?id=<bundle_id>`
   - 功能：根据传入的捆绑包 ID 获取该捆绑包的详细信息，包括捆绑包的总价、折扣、包含的游戏及其 ID。

3. **GitHub 用户API**
   - API 路由：`/api/github/user?id=<user_id>`
   - 功能：根据传入的用户 ID 获取该用户的详细信息，包括头像、简介、关注数以及提交量和发布的代码库数量

4. **GitHub 仓库信息抓取**
   - API 路由：`/api/github/rep?rep=<repo_id>`
   - 功能：根据传入的仓库 ID 获取该仓库的详细信息，包括仓库名称、描述、Star 数量、Fork 数量等。

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

   - **核心依赖（按功能）**：
     - `Flask` 和 `Flask-Cors`：提供 Web 框架和跨域支持。
     - `requests`：处理 HTTP 请求。
     - `beautifulsoup4` 和 `soupsieve`：解析 HTML。
     - `python-dotenv`：加载环境变量。
     - `gunicorn`：用于生产环境部署 Flask。
     - 可能需要的其他实用包：`attrs`, `cattrs`, `url-normalize`。

## 注意事项

- 请确保您的 Python 环境中安装了所有必要的包，最好使用虚拟环境进行隔离。
- 由于爬虫程序涉及从外部网站抓取数据，请确保遵守 Steam 的使用条款和隐私政策，避免对网站产生过大的压力

- 请在`/modules/github/github_user.py`中的`GITHUB_TOKEN = "github_token_test-here"`填写你的token避免github的API调用次数限制