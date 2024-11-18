from flask import Flask, request, jsonify

app = Flask(__name__)

# 프롬프트 생성 함수
def generate_prompt(delta, theta, alpha, gamma):
    if alpha > max(delta, theta, gamma):
        prompt = "A serene and peaceful landscape with soft colors and gentle light."
    elif delta > max(delta, theta, alpha):
        prompt = "A focused and intense abstract pattern with sharp, vivid colors."
    elif gamma > max(delta, theta, alpha):
        prompt = "An energetic and vibrant abstract scene with intricate details."
    elif theta > max(delta, alpha, gamma):
        prompt = "A dreamy and ethereal forest with mist and calm tones."
    else:
        prompt = "A balanced, harmonious scene representing a calm state."
    
    return prompt

# 뇌파 데이터를 받아 프롬프트를 생성하여 응답하는 API 엔드포인트
@app.route('/api/brainwaves/upload', methods=['POST'])
def upload_brainwaves():
    try:
        # 클라이언트로부터 뇌파 데이터 받기
        brainwaves = request.json

        # 뇌파 데이터 추출
        delta = brainwaves.get("Delta", 0)
        theta = brainwaves.get("Theta", 0)
        alpha = brainwaves.get("Alpha", 0)
        gamma = brainwaves.get("Gamma", 0)

        # 프롬프트 생성
        prompt = generate_prompt(delta, theta, alpha, gamma)

        # 프롬프트 응답 반환
        return jsonify({"status": "success", "prompt": prompt}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)



'''
체크해야 하는 점
1. 규민님이 넘겨주는 데이터(json)가 들어오는 엔드포인트가 제대로 지정되지 않은 것 같음
2. 넘겨주는 데이터는 여러개의 값..?을 가지는데 지금은 우선 하나만 들어온다고 가정하고 되어있음.
최댓값/평균값으로 처리하는 함수 필요
3. 프롬프트가 단순해서 1차 생성되는 내용이 겹칠 수 밖에 없어 미술적 가치를 가진다고 보기엔 아직 아쉬움.
변화를 감지하는 등 프롬프트를 다채롭게 만들 수 있는 방법을 생각해야 함.
'''