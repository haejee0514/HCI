import json
import requests
import math

# Flask 백엔드 서버의 IP 주소와 포트번호 설정
#BACKEND_IP = "192.168.0.X"  # Flask 서버의 IP 주소 (여기에 실제 IP 입력)
#BACKEND_PORT = "5000"

# POST 요청으로 뇌파 데이터 전송
#url = f"http://{BACKEND_IP}:{BACKEND_PORT}/api/brainwaves/describe"

# NaN 값을 처리하는 함수
def clean_data(data):
    for key, value in data.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            print(f"{key} 값이 {value}로 처리 불가능. 0으로 대체합니다.")
            data[key] = 0  # NaN 값을 0으로 대체
    return data

# ai_band_data.json 파일 읽기 및 NaN 값 처리
def load_and_clean_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # JSON 파일 읽기
            # NaN 값 처리
            cleaned_data = [clean_data(entry) for entry in data]
            return cleaned_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON decoding failed. Ensure the file is correctly formatted.")
        return None

# JSON 데이터를 백엔드로 전송
def send_to_backend(data, url="http://172.20.39.189:5000/api/brainwaves/describe"):
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

# JSON 파일 경로
file_path = "ai_band_data.json"

# 파일에서 데이터를 로드하고 NaN 값 처리
cleaned_data = load_and_clean_data(file_path)

# 처리된 데이터를 파일로 저장
if cleaned_data:
    with open("cleaned_ai_band_data.json", "w") as file:
        json.dump(cleaned_data, file, indent=4)
    print("NaN 값이 처리된 JSON 파일이 'cleaned_ai_band_data.json'에 저장되었습니다.")

    # 처리된 데이터를 백엔드로 전송
    for entry in cleaned_data:  # 여러 항목이 있을 경우 하나씩 전송
        send_to_backend(entry)
