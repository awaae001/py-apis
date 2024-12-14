from flask import Blueprint, request, jsonify
from modules.github.github_rep import get_repo_details_from_api
from modules.github.github_user import get_user_data_from_api

# 定义 Blueprint
github_dp = Blueprint('github_rep', __name__)

@github_dp.route('/rep', methods=['GET'])
def get_github_repo():
    # 获取查询参数中的 'rep' 和 'extra' 参数
    repo = request.args.get('rep')
    extra_params = request.args.get('extra')

    # 如果没有提供仓库名，则返回错误
    if not repo:
        return jsonify({"error": "缺少仓库参数 'rep'"}), 400

    # 如果提供了 'extra' 参数，将其作为额外数据传递到返回结果中
    result = {
        "repo": repo,
        "extra_params": extra_params
    }

    try:
        # 调用 get_repo_details 获取仓库详情，仅传递仓库名
        repo_details = get_repo_details_from_api(repo)  # 只传递 repo 参数
        result.update(repo_details)  # 合并返回的数据
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"获取仓库详情失败: {str(e)}"}), 500

@github_dp.route('/user', methods=['GET'])
def get_github_user():
    # 获取查询参数中的 'id'
    user_id = request.args.get('id')

    # 如果没有提供用户 ID，则返回错误
    if not user_id:
        return jsonify({"error": "缺少用户参数 'id'"}), 400

    try:
        # 调用 get_user_details 获取用户详情
        user_details = get_user_data_from_api(user_id)
        return jsonify(user_details)
    except Exception as e:
        return jsonify({"error": f"获取用户详情失败: {str(e)}"}), 500