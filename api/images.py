from flask import Flask, request, jsonify, Blueprint
from stable_diffusion import request_image_generation, API_KEY , seed, request_image_modifying
API_KEY= API_KEY
from brainwaves import image_prompt
images_bp = Blueprint('images',__name__)
import requests
import base64



# 기존 이미지 생성 엔드포인트
@images_bp.route('/api/images/generate', methods=['POST'])

def generate_image():
    prompt = request.json.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    response = request_image_generation(prompt)
    return jsonify(response)


# 이미지 수정(Inpainting) 엔드포인트
@images_bp.route('/api/images/modified', methods=['POST'])
def modify_image():
    data = request.json
    additional_prompt = data.get("inputs")
    base64_image=data.get("init_image")
    seed=data.get("seed")
    # 이미지를 수정하는 요청을 보냄
    response = request_image_modifying(base64_image, additional_prompt,seed)

    # Inpainting 처리 결과를 그대로 반환
    return jsonify(response)

