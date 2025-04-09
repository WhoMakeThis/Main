# 🧠 AI CAPTCHA 웹 애플리케이션

# 가상환경 설정 및 패키지 설치
python -m venv venv
venv\Scripts\activate            - Windows

source venv/bin/activate       - Mac/Linux

pip install -r requirements.txt

#플라스크 서버 실행
set FLASK_APP=app

set FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000

실행 후 브라우저에서 http://127.0.0.1:5000 접속
