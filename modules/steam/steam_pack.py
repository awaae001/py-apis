import os
import time
import requests
from bs4 import BeautifulSoup

CACHE_DIR = "./temp"
CACHE_EXPIRY = 7 * 24 * 60 * 60  # 7 天，以秒为单位

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

def get_pack_details(pack_id):
    """
    通过本地缓存的 HTML 文件解析 Steam 捆绑包详情，指定语言为中文。
    """
    try:
        # 构造Steam捆绑包页面的URL和本地缓存文件路径
        url = f"https://store.steampowered.com/bundle/{pack_id}/?l=schinese"
        html_file = os.path.join(CACHE_DIR, f"bundle_{pack_id}.html")
        
        # 检查缓存是否有效
        if not is_cache_valid(html_file):
            # 下载HTML页面并保存到本地
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"缓存已更新: {html_file}")
        else:
            print(f"使用有效的本地缓存: {html_file}")

        # 从本地文件加载HTML
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # 获取捆绑包名称
        pack_name = soup.find('h2', {'class': 'pageheader'})
        if pack_name:
            pack_name = pack_name.text.strip()
        else:
            pack_name = "捆绑包名称未找到"

        # 获取捆绑包描述
        description = soup.find('div', {'id': 'game_area_description'})
        if description:
            description = description.text.strip()
        else:
            description = "无描述"

        # 获取捆绑包价格
        price = soup.find('div', {'class': 'package_totals_area'})
        if price:
            final_price = price.find('div', {'class': 'bundle_final_price_with_discount'})
            original_price = price.find('div', {'class': 'bundle_final_package_price'})
            final_price = final_price.text.strip() if final_price else "未知价格"
            original_price = original_price.text.strip() if original_price else "未知原价"
        else:
            final_price = original_price = "无价格信息"

        # 获取捆绑包其他信息
        details = soup.find('div', {'class': 'game_meta_data'})
        game_type = ""
        developer = ""
        publisher = ""
        languages = ""
        if details:
            type_element = details.find('span', {'data-panel': True})
            game_type = type_element.text.strip() if type_element else ""
            developer_element = details.find('b', string="开发商:")
            developer = developer_element.find_next('a').text.strip() if developer_element else ""
            publisher_element = details.find('b', string="发行商:")
            publisher = publisher_element.find_next('a').text.strip() if publisher_element else ""
            language_element = details.find('span', {'class': 'language_list'})
            if language_element:
                languages = language_element.text.split('列出的语言')[0].strip()

        # 获取功能
        features = []
        feature_elements = soup.find_all('a', {'class': 'game_area_details_specs_ctn'})
        for feature in feature_elements:
            feature_name = feature.find('div', {'class': 'label'})
            if feature_name:
                features.append(feature_name.text.strip())

        # 获取包含的游戏ID
        included_games = []
        game_elements = soup.find_all('a', {'class': 'tab_item_overlay'})
        for game in game_elements:
            game_url = game.get('href')
            game_id = game_url.split('/')[4] if game_url else None
            if game_id:
                included_games.append(game_id)

        result = {
            "pack_id": pack_id,
            "name": pack_name,
            "price": final_price,
            "currency": "CNY",
            "original_price": original_price,
            "description": description,
            "game_type": game_type,
            "developer": developer,
            "publisher": publisher,
            "languages": languages,
            "features": features,
            "included_games": included_games,
        }
        return result
    except requests.RequestException as e:
        return {"error": f"获取捆绑包详情失败: {str(e)}"}
    except Exception as e:
        return {"error": f"解析页面失败: {str(e)}"}
