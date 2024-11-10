import json
import requests

# AI_Input 예시 데이터
AI_Input = {
    "Delta": 0.5,
    "Theta": 0.3,
    "Alpha": 0.2,
    "Gamma": 0.1
}

# JSON 데이터를 백엔드로 전송
def send_to_backend(data, url="http://your-backend-url/api"):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Successfully sent data to the backend!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# 백엔드로 데이터 전송 실행
send_to_backend({"AI_Input": AI_Input})
