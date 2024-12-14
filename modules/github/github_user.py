import requests
from datetime import datetime, timedelta
import os
import time
import json

CACHE_DIR = "./temp"
CACHE_EXPIRY = 24 * 60 * 60  # 1 天，以秒为单位
GITHUB_TOKEN = "github_token_test-here"  # 替换为你的 GitHub Token

# 确保缓存目录存在
os.makedirs(CACHE_DIR, exist_ok=True)

def is_cache_valid(file_path):
    """
    检查缓存文件是否有效
    """
    if not os.path.exists(file_path):
        return False
    file_mtime = os.path.getmtime(file_path)
    current_time = time.time()
    return (current_time - file_mtime) < CACHE_EXPIRY

def make_authenticated_request(url):
    """
    使用 GitHub Token 进行认证的 HTTP GET 请求
    :param url: 请求的 URL
    :return: 响应 JSON 数据或 None（跳过错误的请求）
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 403:  # 速率限制或权限问题
            print(f"请求被限制或无权限访问（403）：{url}")
            return None  # 跳过
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}，跳过 {url}")
        return None

def get_user_data_from_api(user_id):
    """
    通过 GitHub API 获取用户的基本信息和统计数据
    :param user_id: GitHub 用户 ID
    :return: 用户数据字典
    """
    try:
        # 构造缓存文件路径
        cache_file = os.path.join(CACHE_DIR, f"{user_id}_parsed_result.json")
        
        # 如果缓存文件有效，直接读取解析后的数据
        if is_cache_valid(cache_file):
            print(f"使用有效的本地缓存: {cache_file}")
            with open(cache_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        
        print(f"缓存无效或不存在，开始从 GitHub API 获取数据...")

        # 获取用户基本数据
        user_url = f"https://api.github.com/users/{user_id}"
        user_data = make_authenticated_request(user_url)
        if not user_data:  # 如果返回 None，则跳过
            return {"error": f"无法获取用户 {user_id} 的数据（403 或其他问题）"}
        
        # 获取用户仓库数据
        repo_url = user_data.get('repos_url', '')
        repos_data = make_authenticated_request(repo_url)
        if not repos_data:  # 如果返回 None，则继续执行
            repos_data = []

        # 计算 stars 总数和过去一年的提交数量
        stars = 0
        commit_count = 0
        last_year_date = (datetime.now() - timedelta(days=365)).isoformat()

        for repo in repos_data:
            stars += repo.get('stargazers_count', 0)
            commits_url = repo.get('commits_url').split("{/sha}")[0]
            commits_data = make_authenticated_request(f"{commits_url}?since={last_year_date}")
            if commits_data:  # 跳过失败的提交数据请求
                commit_count += len(commits_data)

        # 组装用户数据
        result = {
            "avatar_url": user_data.get('avatar_url', ''),
            "name": user_data.get('name', ''),
            "blog": user_data.get('blog', '未找到'),
            "login": user_data.get('login', ''),
            "setuptime": user_data.get('created_at', ''),
            "followers": user_data.get('followers', 0),
            "following": user_data.get('following', 0),
            "public_repos": user_data.get('public_repos', 0),
            "public_gists": user_data.get('public_gists', 0),
            "stars": stars,
            "commits_last_year": commit_count
        }

        # 缓存解析后的结果
        with open(cache_file, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        print(f"解析结果已缓存: {cache_file}")

        return result

    except Exception as e:
        return {"error": f"解析数据失败: {str(e)}"}
