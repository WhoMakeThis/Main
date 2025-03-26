from flask import Blueprint, jsonify, request
import random, string, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

captcha_bp = Blueprint("captcha", __name__)
CAPTCHA_FOLDER = "app/static/captcha/"

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
    font = ImageFont.truetype("arial.ttf", 36)

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

    filename = f"{text}.png"
    path = os.path.join(CAPTCHA_FOLDER, filename)
    img.save(path)

    return filename

@captcha_bp.route("/generate", methods=["GET"])
def generate_captcha():
    text = generate_random_text()
    filename = create_captcha(text)
    return jsonify({"captcha_url": f"/static/captcha/{filename}", "text": text})

@captcha_bp.route("/verify", methods=["POST"])
def verify_captcha():
    data = request.json
    user_input = data.get("user_input")
    correct_text = data.get("correct_text")

    if user_input and correct_text and user_input.upper() == correct_text:
        return jsonify({"success": True, "message": "CAPTCHA 인증 성공!"})
    return jsonify({"success": False, "message": "CAPTCHA 인증 실패!"})