from flask import Flask, request, send_file, jsonify
import requests
import base64
from io import BytesIO
# app.py 또는 다른 코드 파일
from config import API_KEY

app = Flask(__name__)

# Stable Diffusion API URL
url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
api_key = API_KEY

@app.route('/api/stableDiffusion', methods=['POST'])
def generate_image():
    prompt = request.json.get("prompt")
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "inputs": prompt
    }
    
    # 이미지 생성 요청
    response = requests.post(url, headers=headers, json=payload)

    # 응답 상태 코드 확인
    if response.status_code == 503:  # 모델이 로딩 중
        error_data = response.json() if response.content else {}
        estimated_time = error_data.get("error", "").split('"estimated_time":')[1].split("}")[0] if "estimated_time" in error_data else "N/A"
        
        # 클라이언트에 로딩 상태와 예상 시간을 반환
        return jsonify({
            "status": "loading",
            "estimated_time": float(estimated_time) if estimated_time != "N/A" else None
        }), 503
    
    elif response.status_code == 200:  # 생성 완료
        # 응답이 이미지일 경우
        if response.headers.get('Content-Type', '') == 'image/jpeg':
            # 바이너리 데이터로 받은 이미지를 Base64로 인코딩
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            # 클라이언트에 Base64 인코딩된 이미지 반환
            return jsonify({"generated_image": image_data})
        
        else:
            return jsonify({"error": "Generated image not found in response"}), 400
    else:
        return jsonify({"error": f"Error: {response.status_code}, {response.text}"}), 400
if __name__ == '__main__':
    app.run(debug=True)
