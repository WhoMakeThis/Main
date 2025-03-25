from flask import Flask
from .routes.main import main_bp
from .routes.captcha import captcha_bp

app = Flask(__name__)

# Blueprint 등록 (라우트를 모듈화해서 분리하는 기능)
# 각각의 라우트를 독립된 모듈로 나누고, main.py와 captcha.py에서 정의된 라우트를 app에 연결함
app.register_blueprint(main_bp)
app.register_blueprint(captcha_bp, url_prefix="/api/captcha")