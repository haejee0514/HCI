# 뇌파 데이터 수신 및 프롬프트 변환 API

from flask import Flask, request, jsonify
import json
import requests
from make_prompts import generate_prompt
app = Flask(__name__)


# 뇌파 데이터를 처리하고 프롬프트를 생성하여 다른 API로 전송
def process_brainwaves(brainwaves):
    # 뇌파 데이터 추출
    delta = brainwaves.get("Delta", 0)
    theta = brainwaves.get("Theta", 0)
    alpha = brainwaves.get("Alpha", 0)
    gamma = brainwaves.get("Gamma", 0)

    # 프롬프트 생성
    prompt = generate_prompt(delta, theta, alpha, gamma)

    # 프롬프트를 /api/brainwaves/upload로 전송
    response = send_prompt_to_api(prompt)

    return response

# 프롬프트를 API로 전송하는 함수
def send_prompt_to_api(prompt):
    url = 'http://your-server.com/api/brainwaves/upload'  # 실제 API 엔드포인트 URL로 변경
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': prompt,
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)
    return response

# 뇌파 데이터를 받아 프롬프트를 생성하여 응답하는 API 엔드포인트
@app.route('/api/brainwaves/upload', methods=['POST'])
def upload_brainwaves():
    try:
        # 클라이언트로부터 뇌파 데이터 받기
        brainwaves = request.json

        # 뇌파 데이터 처리 및 프롬프트 생성
        response = process_brainwaves(brainwaves)

        # API 응답 반환
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Prompt sent successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send prompt."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask, request, jsonify

app = Flask(__name__)



# 뇌파 데이터를 받아 프롬프트를 생성하여 응답하는 API 엔드포인트
@app.route('/api/brainwaves/upload', methods=['POST'])
def upload_brainwaves():
    try:
        # 클라이언트로부터 뇌파 데이터 받기
        brainwaves = request.json

        # 뇌파 데이터 추출
        delta = brainwaves.get("Delta", 0)
        theta = brainwaves.get("Theta", 0)
        alpha = brainwaves.get("Alpha", 0)
        gamma = brainwaves.get("Gamma", 0)

        # 프롬프트 생성
        prompt = generate_prompt(delta, theta, alpha, gamma)

        # 프롬프트 응답 반환
        return jsonify({"status": "success", "prompt": prompt}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)