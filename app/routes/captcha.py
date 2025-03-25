from flask import Blueprint, jsonify, request
import random, string, os
from PIL import Image, ImageDraw, ImageFont

captcha_bp = Blueprint("captcha", __name__)
CAPTCHA_FOLDER = "app/static/captcha/"

def generate_random_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_captcha(text):
    img = Image.new('RGB', (150, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 36)
    draw.text((20, 10), text, fill=(0, 0, 0), font=font)

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