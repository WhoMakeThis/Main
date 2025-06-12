from flask import Flask
from .routes.main import main_bp
from .routes.captcha import captcha_bp

app = Flask(__name__)

# 세션에 캡차 정답 저장하도록 수정 -> 세션 비밀키 설정
app.secret_key = "wmt_super_secret_key_123"

# Blueprint 등록 (라우트를 모듈화해서 분리하는 기능)
# 각각의 라우트를 독립된 모듈로 나누고, main.py와 captcha.py에서 정의된 라우트를 app에 연결함
app.register_blueprint(main_bp)
app.register_blueprint(captcha_bp, url_prefix="/api/captcha")