# Muse 2 연결 확인 API

from flask import Flask, jsonify
from pylsl import StreamInlet, resolve_stream

app = Flask(__name__)

def check_muse_connection():
    try:
        # LSL로 Muse 스트림 검색
        streams = resolve_stream('type', 'EEG')
        if streams:
            return True
        else: 
            return False
        
    except Exception as e:
        print(f"Error connecting to Muse: {e}")
        return False

#API 엔드포인트 정의 
@app.route('/api/connect', methods=['GET'])
def connect_muse():
    connected = check_muse_connection()
    return jsonify({"connected": connected})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)