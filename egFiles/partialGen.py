from flask import Flask, request, send_file, jsonify, session
import requests
import base64
from io import BytesIO
import os
from config import API_KEY

app = Flask(__name__)

# Secret key for sessions

# Stable Diffusion Inpainting 모델 URL
url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-inpainting"
api_key = API_KEY  # Hugging Face API 키

# 이미지를 저장할 경로
image_file_path = 'previous_image.png'

@app.route('/inpaint', methods=['POST'])
def inpaint_image():
    try:
        # 클라이언트로부터 프롬프트 받기
        prompt = request.form.get('prompt', "A beautiful sunset in the background")

        # 이전 이미지가 서버에 존재하면 이를 사용
        if os.path.exists(image_file_path):
            with open(image_file_path, 'rb') as f:
                image_data = f.read()  # 이전 이미지를 읽어옴

            # 이미지를 base64로 인코딩
            image_data_base64 = base64.b64encode(image_data).decode("utf-8")
        else:
            return jsonify({"error": "No previous image available"}), 400

        # 클라이언트에서 보낸 마스크 (이미지 수정 영역) 받기
        mask_file = request.files['mask']
        mask_data = base64.b64encode(mask_file.read()).decode("utf-8")

        # API 요청을 위한 데이터 준비
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "inputs": {
                "image": image_data_base64,
                "mask": mask_data,
                "prompt": prompt
            }
        }

        # Inpainting 요청
        response = requests.post(url, headers=headers, json=payload)

        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            modified_image_base64 = result['image']  # 수정된 이미지
            modified_image_data = base64.b64decode(modified_image_base64)
            image = BytesIO(modified_image_data)

            # 수정된 이미지를 서버에 저장 (다음 요청에 사용)
            with open(image_file_path, 'wb') as f:
                f.write(modified_image_data)

            # 수정된 이미지 반환
            return send_file(image, mimetype='image/png')

        else:
            return jsonify({"error": f"Error: {response.status_code}, {response.text}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

'''
주요 변경 사항:
파일 업로드:

request.files['image']와 request.files['mask']를 사용하여 클라이언트에서 전송된 이미지를 받고 있습니다.
이미지와 마스크 파일을 각각 base64로 인코딩하여 Hugging Face API에 전달합니다.
프롬프트:

클라이언트로부터 프롬프트를 받기 위해 request.form.get('prompt')를 사용하고, 기본값을 "A beautiful sunset in the background"로 설정했습니다.
API 요청:

Hugging Face API로 POST 요청을 보내 수정된 이미지를 받아옵니다.
수정된 이미지 반환:

수정된 이미지를 base64로 디코딩한 후 send_file을 사용해 클라이언트에게 반환합니다.
사용 방법:
이 Flask 서버를 실행한 후, 클라이언트에서 이미지와 마스크 파일을 multipart/form-data 형식으로 POST 요청을 보냅니다.
요청에 포함해야 할 필드:
image: 수정할 이미지 파일
mask: 수정할 부분을 나타내는 마스크 이미지 (수정할 부분을 0으로, 나머지는 1로 표시)
prompt: 이미지 수정에 대한 설명 (선택 사항, 기본값은 "A beautiful sunset in the background")


예시 요청:


curl -X POST http://localhost:5000/inpaint \
    -F "image=@image_to_modify.png" \
    -F "mask=@mask_image.png" \
    -F "prompt=A beautiful sunset in the background"


이 코드에서는 Flask를 사용하여 파일을 받아들이고, 수정된 이미지를 클라이언트에 반환하는 방식으로 Stable Diffusion Inpainting 모델을 호출하는 예시를 제공합니다.
'''