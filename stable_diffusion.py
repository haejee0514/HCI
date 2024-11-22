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
        # 응답이 이미지인 경우 바이너리 데이터를 그대로 처리
        if response.headers.get('Content-Type', '') == 'image/jpeg':
            return {"status": "success", "generated_image": response.content}  # 바이너리 데이터 반환
        else:
            return {"status": "error", "error": "Generated image not found in response"}
    
    else:
        return {"status": "error", "error": f"Error: {response.status_code}, {response.text}"}


def request_image_modifying(init_image, prompt, seed, init_strength=0.1, steps=20, cfg_scale=1.0):
    # init_image는 바이너리 이미지 데이터입니다.
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # init_image를 Base64로 인코딩하여 요청에 포함
    init_image_base64 = base64.b64encode(init_image).decode('utf-8')  # 바이너리 이미지를 Base64로 변환
    
    payload = {
        "prompt": prompt,  # 텍스트 프롬프트
        "init_image": init_image_base64,  # 이미 Base64로 인코딩된 기존 이미지
        "seed": seed,  # 랜덤 시드
        "strength": init_strength,  # 기존 이미지 수정 강도 (0~1)
        "num_inference_steps": steps,  # 생성 단계 수
        "guidance_scale": cfg_scale  # 텍스트 반응 강도
    }
    
    # 수정 API 요청
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # 응답이 이미지인 경우
        content_type = response.headers.get('Content-Type', '')
        if content_type.startswith('image/'):
            try:
                # 바이너리 이미지를 그대로 반환
                return {"status": "success", "modified_image": response.content, "seed": seed}
            except Exception as e:
                return {"status": "error", "error": f"Error processing binary image: {e}"}
        else:
            return {"status": "error", "error": f"Unexpected content type: {content_type}"}
    else:
        return {"status": "error", "error": f"Error: {response.status_code}, {response.text}"}