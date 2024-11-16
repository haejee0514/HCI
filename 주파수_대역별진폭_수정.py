import json
import numpy as np
from pylsl import StreamInlet, resolve_stream
import time
from sklearn.decomposition import FastICA

# 주파수 대역 정의 (Hz)
frequency_bands = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 50)
}

# 푸리에 변환 및 대역별 값 계산 함수
def calculate_band_amplitudes(data, fs=256):
    freq = np.fft.rfftfreq(len(data), d=1/fs)  # 주파수 값
    fft_values = np.fft.rfft(data)           # FFT 결과
    amplitude = np.abs(fft_values)           # 주파수 세기 (진폭)

    band_amplitudes = {}
    for band, (low, high) in frequency_bands.items():
        band_indices = np.where((freq >= low) & (freq <= high))
        band_amplitudes[band] = np.mean(amplitude[band_indices])  # 대역 내 평균 진폭 계산
    return band_amplitudes

# ICA 통한 노이즈 제거
def apply_ica(data):
    """
    FastIcA를 사용해 노이즈 제거
    data: (numpy array) EEG신호 데이터 (채널 x 샘플)
    """
    ica = FastICA(n_components = data.shape[0]) # 채널 수에 맞게 설정
    components = ica.fit_transform(data.T) # 독립 성분으로 분리
    cleaned_data = ica.inverse_transform(components).T
    return cleaned_data

# Muse 2 스트림 연결
print("LSL 스트림을 검색 중...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# JSON 데이터를 저장할 리스트
results = []

# 실시간 데이터 처리
print("실시간 데이터 수집 및 분석 시작...")
fs = 256  # 샘플링 주파수 (Muse 2 기본값)
buffer_size = 256  # 한 번에 처리할 데이터 크기
time_interval = 10.0  # 10초 동안 데이터를 수집
start_time = time.time()

# 데이터를 수집할 동안의 평균 계산용 변수
buffered_band_values = {band: [] for band in frequency_bands}

while True:
    # EEG 데이터 수집
    samples, _ = inlet.pull_chunk(timeout=1.0, max_samples=buffer_size)
    if len(samples) == 0:
        continue

    samples = np.array(samples).T[:4]  # 첫 4개의 채널만 사용(전극별로 분리)
    channel_names = ["TP9 (Left Ear)", "AF7 (Frontal Left)", "AF8 (Frontal Right)", "TP10 (Right Ear)"]

    # 채널별 대역별 값 계산 및 버퍼에 저장
    for i, channel_data in enumerate(samples):
        band_amplitudes = calculate_band_amplitudes(channel_data, fs)
        for band, value in band_amplitudes.items():
            buffered_band_values[band].append(value)

    # 10초 간격으로 평균값 계산
    if time.time() - start_time >= time_interval:
        # 대역별 평균값 계산
        averaged_values = {band: np.mean(buffered_band_values[band]) for band in frequency_bands}
        results.append({"AI_Input": averaged_values})

        # 결과 출력
        print(f"5초 동안의 평균 대역별 진폭 값: {averaged_values}")

        # JSON 파일로 저장
        with open("ai_band_data.json", "w") as json_file:
            json.dump(results, json_file, indent=4)

        # 초기화
        start_time = time.time()
        buffered_band_values = {band: [] for band in frequency_bands}

    # 수집한 주파수 값 시각화(굳이없어도되는코드)
   # import matplotlib.pyplot as plt

#    def calculate_band_amplitudes(data, fs=256):
#        freq = np.fft.rfftfreq(len(data), d=1/fs)  # 주파수 값
#        fft_values = np.fft.rfft(data)            # FFT 결과
#        amplitude = np.abs(fft_values)           # 주파수 세기 (진폭)

        # 주파수-진폭 스펙트럼 시각화
#        plt.figure(figsize=(10, 5))
#        plt.plot(freq, amplitude, color='blue')
#        plt.title("Frequency Spectrum")
#        plt.xlabel("Frequency (Hz)")
#        plt.ylabel("Amplitude")
#        plt.grid(True)
#        plt.show()

#        band_amplitudes = {}
#        for band, (low, high) in frequency_bands.items():
#            band_indices = np.where((freq >= low) & (freq <= high))
#            band_amplitudes[band] = np.mean(amplitude[band_indices])  # 대역 내 평균 진폭 계산
#        return band_amplitudes
