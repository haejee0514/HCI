import requests

def generate_image(prompt):
    # Hugging Face API URL (Stable Diffusion 모델)
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    
    # API Token (자신의 토큰으로 교체)
    headers = {
        "Authorization": "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"
    }
    
    # 요청 데이터
    payload = {
        "inputs": prompt
    }
    
    # POST 요청을 보내서 이미지 생성
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        # 성공적으로 이미지 생성되었을 경우
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        print("이미지 생성 완료!")
    else:
        # 오류가 발생한 경우
        print(f"Error: {response.status_code}, {response.text}")

# 예시 실행
generate_image("a fantasy landscape with mountains and a river")
