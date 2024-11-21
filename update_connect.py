import requests
import json

status_data = {"connected": True}  
url = "http://172.20.39.189:5000/api/brainwaves/connect-status"

# post
try:
    response = requests.post(url, json=status_data)
    if response.status_code == 200:
        print("Successfully sent status to the backend!")
    else:
        print(f"Failed to sed. Response code: {response.status_code}")
        print(f"Responde message {response.text}")
except Exception as e:
    print(f"오류 발생: {e}")