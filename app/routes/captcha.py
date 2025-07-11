from flask import Blueprint, jsonify, request, session
import random, string, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from uuid import uuid4
from datetime import datetime

captcha_bp = Blueprint("captcha", __name__)
CAPTCHA_FOLDER = "app/static/captcha/"
# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# 폰트를 static/fonts/ 에 저장, os로 폰트 경로 지정
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "fonts", "DejaVuSans-Bold.ttf"))

def generate_random_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# def create_captcha(text):
#     img = Image.new('RGB', (150, 50), color=(255, 255, 255))
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype("arial.ttf", 36)
#     draw.text((20, 10), text, fill=(0, 0, 0), font=font)

#     filename = f"{text}.png"
#     path = os.path.join(CAPTCHA_FOLDER, filename)
#     img.save(path)
#     return filename

def create_captcha(text):
    width, height = 150, 50
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 36)
    
    # 🔹 글자마다 회전 + 위치 흔들기
    x = 5
    for char in text:
        y_offset = random.randint(0, 10)
        angle = random.randint(-30, 30)

        # 1. 글자용 이미지 생성
        char_img = Image.new('RGBA', (40, 40), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, font=font, fill=(0, 0, 0))

        # 2. 회전 적용
        rotated = char_img.rotate(angle, expand=1)

        # 3. 원래 이미지에 붙이기
        img.paste(rotated, (x, y_offset), rotated)
        x += 25

    # 🔹 랜덤 선 추가
    for _ in range(5):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = tuple(random.randint(0, 255) for _ in range(3))
        draw.line((x1, y1, x2, y2), fill=color, width=1)

    # 🔹 랜덤 점 추가
    for _ in range(100):
        x_dot, y_dot = random.randint(0, width), random.randint(0, height)
        color = tuple(random.randint(0, 255) for _ in range(3))
        draw.point((x_dot, y_dot), fill=color)

    # 🔹 블러 필터(선택)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))

#    파일명에 정답 노출
#    filename = f"{text}.png"
#    path = os.path.join(CAPTCHA_FOLDER, filename)
#    img.save(path)
#
#    return filename

    # 파일명 uuid로 저장
    filename = f"{uuid4().hex}.png"
    path = os.path.join(CAPTCHA_FOLDER, filename)
    img.save(path)

    return filename

@captcha_bp.route("/generate", methods=["GET"])
def generate_captcha():
    text = generate_random_text()
    filename = create_captcha(text)
#   return jsonify({"captcha_url": f"/static/captcha/{filename}", "text": text})
    session["captcha_answer"] = text  # 정답은 서버 세션에 저장
    session["captcha_start_time"] = datetime.now().isoformat() # 응답 시간 분석
    return jsonify({"captcha_url": f"/static/captcha/{filename}"})


@captcha_bp.route("/verify", methods=["POST"])
def verify_captcha():
    data = request.json
    user_input = data.get("user_input")
#   correct_text = data.get("correct_text")
    correct_text = session.get("captcha_answer")

    # 응답 시간 1초 미만이면 봇 판단
    start_time_str = session.get("captcha_start_time")
    if start_time_str:
        start_time = datetime.fromisoformat(start_time_str)
        elapsed = (datetime.now() - start_time).total_seconds()
    else:
        elapsed = None

    if elapsed is not None and elapsed < 1.0:
        return jsonify({"success": False, "message": "⚠ 응답 시간이 너무 빨라 차단되었습니다."})

    if user_input and correct_text and user_input.upper() == correct_text:
        return jsonify({"success": True, "message": "CAPTCHA 인증 성공!"})
    return jsonify({"success": False, "message": "CAPTCHA 인증 실패!"})
