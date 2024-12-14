import os
from flask import Flask
from routes.steam import steam_bp
from routes.github import github_dp

app = Flask(__name__)
# GITHUB_TOKEN = os.getenv('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')

# 注册蓝图
app.register_blueprint(steam_bp, url_prefix='/api/steam')
app.register_blueprint(github_dp, url_prefix='/api/github')
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)