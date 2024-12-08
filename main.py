from flask import Flask
from routes.steam import steam_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(steam_bp, url_prefix='/api/steam')
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
