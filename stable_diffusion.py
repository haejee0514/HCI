# Stable Diffusion 호출 API

import sys
import os
import random
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
    if response.status_code == 200:
        # 정상적인 이미지 응답 처리
        if response.headers.get('Content-Type', '') == 'image/jpeg':
            image_data = base64.b64encode(response.content).decode('utf-8')
            return {"status": "success", "generated_image": image_data}
        else:
            return {"status": "error", "error": "Generated image not found in response"}

    else:
        # 500이나 다른 상태 코드에 대한 일반적인 에러 처리
        try:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
        except Exception as e:
            error_message = f"Error parsing response: {e}"

        return {"status": "error", "error": f"Error: {response.status_code}, {error_message}"}


import base64
import requests

def request_image_modifying(init_image, prompt, init_strength=0.1, steps=20, cfg_scale=5.0):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,  # 텍스트 프롬프트
        "init_image": init_image,  # 이미 Base64로 인코딩된 기존 이미지
        "strength": init_strength,  # 기존 이미지 수정 강도 (0~1)
        "num_inference_steps": steps,  # 생성 단계 수
        "guidance_scale": cfg_scale  # 텍스트 반응 강도
    }

    
    print(payload)

    # 이미지 생성 API 요청
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
    

    if response.status_code == 200:
        # 정상적인 이미지 응답 처리
        if response.headers.get('Content-Type', '') == 'image/jpeg':
            image_data = base64.b64encode(response.content).decode('utf-8')
            return {"status": "success", "modified_image": image_data}
        else:
            return {"status": "error", "error": "Generated image not found in response"}

    else:
        # 500이나 다른 상태 코드에 대한 일반적인 에러 처리
        try:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
        except Exception as e:
            error_message = f"Error parsing response: {e}"

        return {"status": "error", "error": f"Error: {response.status_code}, {error_message}"}