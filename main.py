import requests
import json
import numpy as np
from pylsl import StreamInlet, resolve_stream
import time
from sklearn.decomposition import FastICA
import math

# Step 1: Muse2 연결 상태 업데이트
def update_connection_status():
    status_data = {"connected": True}  # 연결 상태 데이터
    url = "http://172.30.1.66:5000/api/brainwaves/connect-status"  # 백엔드 API URL

    try:
        response = requests.post(url, json=status_data)
        if response.status_code == 200:
            print("Successfully sent status to the backend!0")
        else:
            print(f"Failed to send. Responde code: {response.status_code}")
            print(f"Response  message : {response.text}")
    except Exception as e:
        print(f"오류 발생: {e}")

# Step 2: 뇌파 데이터 처리 및 JSON 저장
def process_brainwave_data():
    # 주파수 대역 정의
    frequency_bands = {
        "Delta": (0.5, 4),
        "Theta": (4, 8),
        "Alpha": (8, 13),
        "Beta": (13, 30),
        "Gamma": (30, 50)
    }

    # 대역별 진폭 계산 함수
    def calculate_band_amplitudes(data, fs=256):
        freq = np.fft.rfftfreq(len(data), d=1/fs)
        fft_values = np.fft.rfft(data)
        amplitude = np.abs(fft_values)

        band_amplitudes = {}
        for band, (low, high) in frequency_bands.items():
            band_indices = np.where((freq >= low) & (freq <= high))
            band_amplitudes[band] = np.mean(amplitude[band_indices])
        return band_amplitudes

    # ICA를 이용한 노이즈 제거 함수
    def apply_ica(data):
        ica = FastICA(n_components=data.shape[0])
        components = ica.fit_transform(data.T)
        cleaned_data = ica.inverse_transform(components).T
        return cleaned_data

    print("LSL 스트림 검색 중...")
    streams = resolve_stream('type', 'EEG')  # LSL 스트림 검색
    inlet = StreamInlet(streams[0])

    results = []  # 처리된 데이터를 저장할 리스트
    fs = 256  # 샘플링 주파수
    buffer_size = 256  # 한 번에 처리할 데이터 크기
    time_interval = 10.0  # 10초 동안 데이터를 수집
    start_time = time.time()

    buffered_band_values = {band: [] for band in frequency_bands}

    # 데이터 수집
    while time.time() - start_time < time_interval:
        samples, _ = inlet.pull_chunk(timeout=1.0, max_samples=buffer_size)
        if len(samples) == 0:
            continue

        samples = np.array(samples).T[:4]  # 첫 4개 채널만 사용
        for channel_data in samples:
            band_amplitudes = calculate_band_amplitudes(channel_data, fs)
            for band, value in band_amplitudes.items():
                buffered_band_values[band].append(value)

    # 대역별 평균값 계산
    averaged_values = {band: np.mean(buffered_band_values[band]) for band in frequency_bands}
    print(f"10초 동안의 평균 대역별 진폭 값: {averaged_values}")

    # 결과 JSON으로 저장
    with open("ai_band_data.json", "w") as json_file:
        json.dump([averaged_values], json_file, indent=4)

# Step 3: 처리된 데이터 정리 및 백엔드 전송
def clean_and_send_data():
    def clean_data(data):
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0.0  # NaN 값을 0으로 대체
            elif isinstance(value, float):  # 소수점 한 자리로 제한
                data[key] = round(value, 1)
        return data

    # JSON 데이터 읽기 및 NaN 값 처리
    try:
        with open("ai_band_data.json", "r") as file:
            data = json.load(file)
        cleaned_data = [clean_data(entry) for entry in data]

        # 정리된 데이터를 저장
        with open("cleaned_ai_band_data.json", "w") as cleaned_file:
            json.dump(cleaned_data, cleaned_file, indent=4)
        print("정리된 데이터가 cleaned_ai_band_data.json에 저장되었습니다.")
    except Exception as e:
        print(f"데이터 정리 오류: {e}")
        return

    # 정리된 데이터를 백엔드로 전송
    url = "http://172.30.1.66:5000/api/brainwaves/describe"
    headers = {'Content-Type': 'application/json'}
    for entry in cleaned_data:
        try:
            response = requests.post(url, json=entry, headers=headers)
            if response.status_code == 200:
                print("백엔드로 데이터 전송 성공!")
            else:
                print(f"전송 실패. 응답 코드: {response.status_code}")
                print(f"응답 메시지: {response.text}")
        except Exception as e:
            print(f"데이터 전송 중 오류 발생: {e}")

# 통합 실행
if __name__ == "__main__":
    update_connection_status()  # Step 1: 연결 상태 업데이트
    process_brainwave_data()    # Step 2: 뇌파 데이터 처리
    clean_and_send_data()       # Step 3: 데이터 정리 및 전송
