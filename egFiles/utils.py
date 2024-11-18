import json
import os
from config import DATA_DIR

# EEG 데이터 저장
def save_brainwave_data(data):
    json_path = os.path.join(DATA_DIR, 'eeg.json')
    with open(json_path, 'w') as file:
        json.dump(data, file)

# EEG 데이터 불러오기
def load_brainwave_data():
    json_path = os.path.join(DATA_DIR, 'eeg.json')
    if not os.path.exists(json_path):
        return None
    with open(json_path, 'r') as file:
        return json.load(file)