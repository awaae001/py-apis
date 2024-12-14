import os
import time
import requests

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

def get_repo_details_from_api(repo_full_name):
    """
    通过 GitHub API 获取仓库详情。
    :param repo_full_name: 仓库全名 (例如: 'ArtalkJS/Artalk')
    """
    try:
        # 构造 GitHub API 的 URL
        url = f"https://api.github.com/repos/{repo_full_name}"

        # 尝试使用缓存
        html_file = os.path.join(CACHE_DIR, f"{repo_full_name.replace('/', '_')}.json")
        
        # 检查缓存是否有效
        if not is_cache_valid(html_file):
            # 发送请求获取数据
            response = requests.get(url, timeout=10, allow_redirects=True)
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
        
        # 获取仓库相关数据
        repo_name = data.get('name', '仓库名称未找到')
        stars = data.get('stargazers_count', 0)
        latest_commit_time = data.get('pushed_at', '未知时间')
        description = data.get('description', '无描述')
        forks = data.get('forks_count', 0)
        open_issues = data.get('open_issues_count', 0)

        # 组装结果
        result = {
            "repo_name": repo_name,
            "stars": stars,
            "latest_commit_time": latest_commit_time,
            "description": description,
            "forks": forks,
            "open_issues": open_issues
        }

        return result

    except requests.RequestException as e:
        return {"error": f"获取仓库详情失败: {str(e)}"}
    except Exception as e:
        return {"error": f"解析数据失败: {str(e)}"}