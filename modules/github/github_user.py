import requests
from datetime import datetime, timedelta
import os
import time
import json

CACHE_DIR = "./temp"
CACHE_EXPIRY = 24 * 60 * 60  # 1 天，以秒为单位

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
        # 构造缓存文件路径
        cache_file = os.path.join(CACHE_DIR, f"{user_id}_parsed_result.json")
        
        # 如果缓存文件有效，直接读取解析后的数据
        if is_cache_valid(cache_file):
            print(f"使用有效的本地缓存: {cache_file}")
            with open(cache_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        
        print(f"缓存无效或不存在，开始从 GitHub API 获取数据...")

        # 构造 GitHub API 的 URL
        user_url = f"https://api.github.com/users/{user_id}"

        # 获取用户信息
        user_response = requests.get(user_url, timeout=10)
        user_response.raise_for_status()
        user_data = user_response.json()

        # 获取用户仓库信息
        repo_url = user_data.get('repos_url', '')
        repo_response = requests.get(repo_url, timeout=10)
        repo_response.raise_for_status()
        repos_data = repo_response.json()

        # 计算用户的 stars 总数和过去一年的提交量
        stars = 0
        commit_count = 0
        last_year_date = (datetime.now() - timedelta(days=365)).isoformat()

        for repo in repos_data:
            # 累计 stars 数量
            stars += repo.get('stargazers_count', 0)

            # 累计过去一年的提交数
            commits_url = repo.get('commits_url', '').split("{/sha}")[0]
            commits_response = requests.get(f"{commits_url}?since={last_year_date}", timeout=10)
            commits_response.raise_for_status()
            commits_data = commits_response.json()
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
        print(f"解析结果已缓存到: {cache_file}")

        return result

    except requests.RequestException as e:
        return {"error": f"获取用户数据失败: {str(e)}"}
    except Exception as e:
        return {"error": f"解析数据失败: {str(e)}"}
