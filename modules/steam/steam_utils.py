import requests

def get_game_details(game_id):
    """
    通过 Steam API 获取游戏详情，并指定语言为中文
    """
    try:
        # 设置请求头，告诉 Steam 返回中文内容
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        
        # 构造Steam API的URL
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get(str(game_id), {}).get("success"):
            game_data = data[str(game_id)]["data"]
            result = {
                "game_id": game_id,
                "name": game_data.get("name"),
                "price": game_data.get("price_overview", {}).get("final_formatted", "免费"),
                "currency": game_data.get("price_overview", {}).get("currency", "未知"),
                "description": game_data.get("short_description", ""),
                "release_date": game_data.get("release_date", {}).get("date", "未知"),
                "developer": game_data.get("developers", ["未知"])[0],
                "publisher": game_data.get("publishers", ["未知"])[0],
                "platforms": game_data.get("platforms", {}),
                "categories": [cat["description"] for cat in game_data.get("categories", [])],
                "genres": [genre["description"] for genre in game_data.get("genres", [])],
            }
            return result
        else:
            return {"error": "游戏未找到或不可用。"}
    except requests.RequestException as e:
        return {"error": f"获取游戏详情失败: {str(e)}"}
