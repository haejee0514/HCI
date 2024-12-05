import requests
import base64
from PIL import Image
from io import BytesIO
import time

# Hugging Face API URL (예시)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
from config import API_KEY

# 이미지를 URL로 불러오기
def load_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

# 이미지를 Base64로 인코딩
def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# 이미지와 프롬프트로 API 요청 보내기
def request_image_modification(prompt, init_image_url, seed=None, max_retries=5, retry_delay=120):
    # 초기 이미지 불러오기
    init_image = load_image_from_url(init_image_url)
    init_image_base64 = encode_image_to_base64(init_image)

    # 요청 payload 준비
    payload = {
        "inputs": prompt,
        "init_image": init_image_base64,
        "seed": seed
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    retry_count = 0

    while retry_count < max_retries:
        # API 요청 보내기
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            # 정상적으로 이미지가 생성된 경우
            result = response.json()
            generated_image_data = result.get('image')  # 이미지는 Base64로 반환
            generated_image = Image.open(BytesIO(base64.b64decode(generated_image_data)))
            generated_image.show()  # 이미지 표시
            return {"status": "success", "generated_image": generated_image}
        
        elif response.status_code == 503:
            # 모델이 로딩 중인 경우
            error_message = response.json().get("error", "")
            if "model is loading" in error_message:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"모델이 로딩 중입니다. {retry_delay}초 후에 재시도합니다... (시도 {retry_count}/{max_retries})")
                    time.sleep(retry_delay)  # 대기 후 재시도
                else:
                    return {"status": "error", "error": "모델 로딩이 너무 오래 걸리고 있습니다. 나중에 다시 시도하세요."}
            else:
                return {"status": "error", "error": "모델 상태를 확인할 수 없습니다."}
        
        else:
            # 기타 상태 코드에 대한 에러 처리
            try:
                error_data = response.json()
                error_message = error_data.get("error", "Unknown error")
            except Exception as e:
                error_message = f"Error parsing response: {e}"

            return {"status": "error", "error": f"Error: {response.status_code}, {error_message}"}
    
    # 재시도 횟수 초과 시
    return {"status": "error", "error": "모델 로딩 시간 초과. 나중에 다시 시도해주세요."}

# 예시 호출
prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
init_image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/img2img-init.png"
response = request_image_modification(prompt, init_image_url)

print(response)
