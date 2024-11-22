from flask import Flask, request, jsonify, Blueprint
from stable_diffusion import request_image_generation, API_KEY , seed, request_image_modifying
import sys
import os
# 현재 파일의 디렉토리를 기준으로 상위 디렉토리를 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from brainwaves import image_prompt
API_KEY= API_KEY

import requests
import base64

from io import BytesIO
from flask import send_file


base_image=None
seed=None

images_bp = Blueprint('images',__name__)
# 기존 이미지 생성 엔드포인트
@images_bp.route('/api/images/generate', methods=['GET'])

def generate_image():
    global base_image
    global image_prompt
    print(image_prompt)
    # 이미지 생성 요청
    response = request_image_generation(image_prompt)

    if response.get("status") == "success":
        base_image = response.get("generated_image")
        
        # 바이너리 이미지 데이터를 클라이언트로 전송
        return send_file(BytesIO(base_image), mimetype='image/jpeg', as_attachment=False, download_name='generated_image.jpg')
    else:
        return jsonify(response), 400



# 이미지 수정(Inpainting) 엔드포인트
@images_bp.route('/api/images/modified', methods=['POST'])
def modify_image():
    global seed
    global base_image
    data = request.json
    additional_prompt = data.get("inputs")
    # 이미지를 수정하는 요청을 보냄
    response = request_image_modifying(base_image, additional_prompt,seed)

    # Inpainting 처리 결과를 그대로 반환
    return jsonify(response)