from flask import Flask
from views.account.views import account_blue
from views.ota.views import ota_blue
import os

app = Flask(__name__)
# 上传文件目录配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/upload')

app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(account_blue)
app.register_blueprint(ota_blue)

if __name__ == '__main__':
    app.run()
