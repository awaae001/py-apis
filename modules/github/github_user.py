import requests
from datetime import datetime, timedelta
import os
import time

CACHE_DIR = "./temp"
CACHE_EXPIRY = 24 * 60 * 60  # 1 天，以秒为单位

# GitHub Token 设置
GITHUB_TOKEN = "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"  # 将此处替换为你的 GitHub Token

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

def get_user_data_from_api(user_id):
    """
    通过 GitHub API 获取用户的基本信息和统计数据
    :param user_id: GitHub 用户 ID
    :return: 用户数据字典
    """
    try:
        # 构造 GitHub API 的 URL
        url = f"https://api.github.com/users/{user_id}"

        # 设置请求头，加入 GitHub Token
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # 尝试使用缓存
        html_file = os.path.join(CACHE_DIR, f"{user_id}_user_info.json")
        
        # 检查缓存是否有效
        if not is_cache_valid(html_file):
            # 发送请求获取数据
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            data = response.json()
            # 保存到缓存文件
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"缓存已更新: {html_file}")
        else:
            print(f"使用有效的本地缓存: {html_file}")
            # 从缓存文件加载数据
            with open(html_file, 'r', encoding='utf-8') as file:
                data = file.read()
            data = eval(data)  # 将文件中的字符串恢复为字典对象
        
        # 获取用户基本数据
        avatar_url = data.get('avatar_url', '')
        name = data.get('name', '')
        login = data.get('login', '')
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        public_repos = data.get('public_repos', 0)
        public_gists = data.get('public_gists', 0)
        stars = 0  # stars 数量暂时为 0，稍后通过仓库统计计算

        # 获取用户仓库数据
        repo_url = data.get('repos_url', '')
        repos_response = requests.get(repo_url, headers=headers, timeout=10)
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        # 计算用户的 stars 总数
        for repo in repos_data:
            stars += repo.get('stargazers_count', 0)

        # 获取过去一年的提交量
        last_year_date = (datetime.now() - timedelta(days=365)).isoformat()
        commit_count = 0
        for repo in repos_data:
            commits_url = repo.get('commits_url').split("{/sha}")[0]  # 去掉 {sha} 部分
            commits_response = requests.get(f"{commits_url}?since={last_year_date}", headers=headers, timeout=10)
            commits_response.raise_for_status()
            commits_data = commits_response.json()
            commit_count += len(commits_data)

        # 组装用户数据
        result = {
            "avatar_url": avatar_url,
            "name": name,
            "login": login,
            "followers": followers,
            "following": following,
            "public_repos": public_repos,
            "public_gists": public_gists,
            "stars": stars,
            "commits_last_year": commit_count
        }

        return result

    except requests.RequestException as e:
        return {"error": f"获取用户数据失败: {str(e)}"}
    except Exception as e:
        return {"error": f"解析数据失败: {str(e)}"}

