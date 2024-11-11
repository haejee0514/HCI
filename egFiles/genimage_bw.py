from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# /api/brainwaves/upload 엔드포인트
@app.route('/api/brainwaves/upload', methods=['POST'])
def process_brainwaves():
    # JSON 데이터 수신
    data = 'data/eeg.json'
    with open(data, 'r') as file:
        brainwaves = json.load(file)
    
    # 뇌파 데이터 추출
    delta = brainwaves.get("Delta", 0)
    theta = brainwaves.get("Theta", 0)
    alpha = brainwaves.get("Alpha", 0)
    gamma = brainwaves.get("Gamma", 0)

    # 뇌파 데이터를 기반으로 프롬프트 생성
    prompt = generate_prompt(delta, theta, alpha, gamma)

    # Stable Diffusion API 호출
    image_data = call_stable_diffusion(prompt)

    # 응답 반환 (Base64로 인코딩된 이미지)
    return jsonify({"prompt": prompt, "image_data": image_data})

# 프롬프트 생성 함수
def generate_prompt(delta, theta, alpha, gamma):
    # 예시 프롬프트 생성 로직
    if alpha > max(delta, theta, gamma):
        prompt = "A serene and peaceful landscape with soft colors and gentle light."
    elif delta > max(delta, theta, alpha):
        prompt = "A focused and intense abstract pattern with sharp, vivid colors."
    elif gamma > max(delta, theta, alpha):
        prompt = "An energetic and vibrant abstract scene with intricate details."
    elif theta > max(delta, alpha, gamma):
        prompt = "A dreamy and ethereal forest with mist and calm tones."
    else:
        prompt = "A balanced, harmonious scene representing a calm state."

    return prompt

# Stable Diffusion 호출 함수 수정
def call_stable_diffusion(prompt):
    # Stable Diffusion API 엔드포인트
    stable_diffusion_api_url = "http://localhost:5000/api/stableDiffusion"  # genimage.py 서버 URL
    
    # API 요청 데이터 생성
    payload = {"prompt": prompt}
    
    # Stable Diffusion API 호출
    response = requests.post(stable_diffusion_api_url, json=payload)
    
    # 응답 처리
    if response.status_code == 200:
        # 생성된 이미지 URL 반환 (응답 본문에 포함된 URL을 반환)
        return response.json().get("image_url")
    else:
        # 오류 발생 시 None 반환
        return None


if __name__ == '__main__':
    app.run(debug=True)
