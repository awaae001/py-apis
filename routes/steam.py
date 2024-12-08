from flask import Blueprint, request, jsonify
from modules.steam_utils import get_game_details
from modules.steam_pack import get_pack_details

steam_bp = Blueprint('steam', __name__)

# 获取游戏信息的路由
@steam_bp.route('/game', methods=['GET'])
def get_game():
    game_id = request.args.get('gameid')
    if not game_id:
        return jsonify({"error": "Missing 'gameid' parameter"}), 400
    
    game_details = get_game_details(game_id)
    return jsonify(game_details)

# 获取捆绑包信息的路由
@steam_bp.route('/pack', methods=['GET'])
def get_pack():
    pack_id = request.args.get('id')
    if not pack_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400
    
    pack_details = get_pack_details(pack_id)
    return jsonify(pack_details)
