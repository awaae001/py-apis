import requests
from bs4 import BeautifulSoup

def get_pack_details(pack_id):
    """
    通过 Steam 网页获取捆绑包详情，并指定语言为中文
    """
    try:
        # 构造Steam捆绑包页面的URL
        url = f"https://store.steampowered.com/bundle/{pack_id}/?l=schinese"
        
        # 发送请求，确保允许重定向
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # 解析页面
        soup = BeautifulSoup(response.text, 'html.parser')

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
            # 提取最终价格和折扣价格
            final_price = price.find('div', {'class': 'bundle_final_price_with_discount'})
            original_price = price.find('div', {'class': 'bundle_final_package_price'})
            if final_price:
                final_price = final_price.text.strip()
            else:
                final_price = "未知价格"
            if original_price:
                original_price = original_price.text.strip()
            else:
                original_price = "未知原价"
        else:
            final_price = original_price = "无价格信息"

        # 获取捆绑包详细信息（类型、开发商、发行商、语言）
        details = soup.find('div', {'class': 'game_meta_data'})
        game_type = ""
        developer = ""
        publisher = ""
        languages = ""
        if details:
            # 获取类型
            type_element = details.find('span', {'data-panel': True})
            if type_element:
                game_type = type_element.text.strip()
            
            # 获取开发商
            developer_element = details.find('b', string="开发商:")
            if developer_element:
                developer = developer_element.find_next('a').text.strip()
            
            # 获取发行商
            publisher_element = details.find('b', string="发行商:")
            if publisher_element:
                publisher = publisher_element.find_next('a').text.strip()
            
            # 获取语言
            language_element = details.find('span', {'class': 'language_list'})
            if language_element:
                languages = language_element.text.strip()
                # 只提取语言名称，去除额外描述文字
                languages = languages.split('列出的语言')[0].strip()

        # 获取捆绑包包含的功能
        features = []
        feature_elements = soup.find_all('a', {'class': 'game_area_details_specs_ctn'})
        for feature in feature_elements:
            feature_name = feature.find('div', {'class': 'label'})
            if feature_name:
                features.append(feature_name.text.strip())

        # 获取捆绑包包含的游戏ID（通过 <a class="tab_item_overlay" href="..."> 标签）
        included_games = []
        game_elements = soup.find_all('a', {'class': 'tab_item_overlay'})
        for game in game_elements:
            game_url = game.get('href')  # 获取游戏的URL
            game_id = game_url.split('/')[4] if game_url else None  # 提取游戏ID
            if game_id:
                included_games.append(game_id)

        result = {
            "pack_id": pack_id,
            "name": pack_name,
            "price": final_price,
            "currency": "CNY",  # 假设是人民币
            "original_price": original_price,  # 包括原价
            "description": description,
            "game_type": game_type,
            "developer": developer,
            "publisher": publisher,
            "languages": languages,
            "features": features,
            "included_games": included_games,  # 返回游戏ID
        }
        return result
    except requests.RequestException as e:
        return {"error": f"获取捆绑包详情失败: {str(e)}"}
    except Exception as e:
        return {"error": f"解析页面失败: {str(e)}"}
