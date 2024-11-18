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

seed = random.randint(0, 1000000)

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


def request_image_modifying(init_image, prompt, seed, init_strength=0.1, steps=20, cfg_scale=1.0):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,  # 텍스트 프롬프트
        "init_image": init_image,  # base64로 인코딩된 기존 이미지
        "seed": seed,  # 랜덤 시드
        "strength": init_strength,  # 기존 이미지 수정 강도 (0~1)
        "num_inference_steps": steps,  # 생성 단계 수
        "guidance_scale": cfg_scale  # 텍스트 반응 강도
    }
    
    # 수정 API 요청
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # API 응답이 이미지인지 확인
        if 'image/' in response.headers.get('Content-Type', ''):
            try:
                image_data = base64.b64encode(response.content).decode('utf-8')  # 수정된 이미지를 base64로 변환
                return {"status": "success", "modified_image": image_data, "seed": seed}
            except Exception as e:
                return {"status": "error", "error": f"Base64 encoding failed: {e}"}
        else:
            return {"status": "error", "error": f"Unexpected content type: {response.headers.get('Content-Type', '')}"}
    else:
        return {"status": "error", "error": f"Error: {response.status_code}, {response.text}"}