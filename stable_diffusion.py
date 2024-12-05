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
# 요청을 최대 재시도 횟수 설정
MAX_RETRIES = 5
RETRY_DELAY = 30  # 대기 시간 (초)


# 첫 번째 요청을 보내어 모델 로딩
def pre_load_model():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "inputs": "A simple test to load the model",
    }

    # 첫 번째 요청 보내기 (모델 로딩 효과)
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        print("모델이 로딩되었습니다.")
    else:
        print(f"API 호출 실패: {response.status_code}, {response.text}")




def request_image_generation(prompt,seed):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "inputs": prompt,
        "seed": seed
    }
    
    retry_count = 0

    while retry_count < MAX_RETRIES:
        # 이미지 생성 API 요청
        response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            # 정상적인 이미지 응답 처리
            if response.headers.get('Content-Type', '') == 'image/jpeg':
                image_data = base64.b64encode(response.content).decode('utf-8')
                return {"status": "success", "generated_image": image_data}
            else:
                return {"status": "error", "error": "Generated image not found in response"}

        elif response.status_code == 503:
            # 서버가 준비되지 않은 경우, 30초 대기 후 재시도
            retry_count += 1
            print(f"Model is loading, retrying {retry_count}/{MAX_RETRIES} in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            # 503 외의 다른 상태 코드 처리
            try:
                error_data = response.json()
                error_message = error_data.get("error", "Unknown error")
            except Exception as e:
                error_message = f"Error parsing response: {e}"

            return {"status": "error", "error": f"Error: {response.status_code}, {error_message}"}
    
    # 최대 재시도 횟수에 도달한 경우
    return {"status": "error", "error": "Max retries reached. The model might be overloaded or unavailable."}


import base64
import requests
import time

# 마지막 요청 시간 추적
last_request_time = 0
request_timeout = 30  # 30초 간격 설정



def request_image_modifying(init_image, prompt, seed, init_strength=0.1, steps=20, cfg_scale=1.0):
    global last_request_time

    # 현재 시간 가져오기
    current_time = time.time()

    # 30초 이내에 이미 요청이 있었다면 두 번째 요청 무시
    if current_time - last_request_time < request_timeout:
        return {"status": "error", "error": "Request ignored. Please wait 30 seconds between requests."}

    # 요청을 처리할 때마다 마지막 요청 시간을 갱신
    last_request_time = current_time

    
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,  # 텍스트 프롬프트
        "init_image": init_image,  # 이미 Base64로 인코딩된 기존 이미지
        "strength": init_strength,  # 기존 이미지 수정 강도 (0~1)
        "num_inference_steps": steps,  # 생성 단계 수
        "guidance_scale": cfg_scale,  # 텍스트 반응 강도
        "seed": seed  # Seed 값을 추가
    }

    retries = 0  # 재시도 횟수 카운터

    while retries < MAX_RETRIES:
        # 이미지 생성 API 요청
        response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
        
        # 응답 상태 처리
        if response.status_code == 200:
            # 정상적인 이미지 응답 처리
            if response.headers.get('Content-Type', '') == 'image/jpeg':
                image_data = base64.b64encode(response.content).decode('utf-8')
                return {"status": "success", "modified_image": image_data}
            else:
                return {"status": "error", "error": "Generated image not found in response"}
        
        elif response.status_code == 503:
            # 503 상태 코드 처리 (서버 과부하 또는 모델 로딩 중)
            print(f"503 Service Unavailable. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)  # 대기 후 재시도
            retries += 1
        else:
            # 500이나 다른 상태 코드에 대한 일반적인 에러 처리
            try:
                error_data = response.json()
                error_message = error_data.get("error", "Unknown error")
            except Exception as e:
                error_message = f"Error parsing response: {e}"

            return {"status": "error", "error": f"Error: {response.status_code}, {error_message}"}
    
    # 재시도 횟수를 초과하면 에러 메시지 반환
    return {"status": "error", "error": "Max retries reached. Please try again later."}