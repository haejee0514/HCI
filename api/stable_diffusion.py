# Stable Diffusion 호출 API

import sys
import os

# 현재 파일의 디렉토리를 기준으로 상위 디렉토리를 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import base64
from config import API_KEY


STABLE_DIFFUSION_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
API_KEY = API_KEY

def request_image_generation(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "inputs": prompt
    }
    
    # 이미지 생성 API 요청
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
    
    # 응답 상태 처리
    if response.status_code == 503:
        error_data = response.json() if response.content else {}
        estimated_time = error_data.get("error", "").split('"estimated_time":')[1].split("}")[0] if "estimated_time" in error_data else None
        return {
            "status": "loading",
            "estimated_time": float(estimated_time) if estimated_time else None
        }
    
    elif response.status_code == 200:
        # API 응답이 이미지일 경우 Base64로 인코딩
        if response.headers.get('Content-Type', '') == 'image/jpeg':
            image_data = base64.b64encode(response.content).decode('utf-8')
            return {"status": "success", "generated_image": image_data}
        else:
            return {"status": "error", "error": "Generated image not found in response"}
    
    else:
        return {"status": "error", "error": f"Error: {response.status_code}, {response.text}"}
# Stable Diffusion 호출 API