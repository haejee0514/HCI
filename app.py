from flask import Flask, request, jsonify, send_file
from tempfile import NamedTemporaryFile

app = Flask(__name__)
'''
# Stable Diffusion 모델 로드
pipe = load_stable_diffusion()

@app.route('/api/brainwaves/upload', methods=['POST'])
def upload_brainwave_data():
    brainwave_data = request.json
    save_brainwave_data(brainwave_data)
    return jsonify({"message": "Brainwave data uploaded successfully"}), 201

@app.route('/api/stableDiffusion', methods=['POST'])
def stable_diffusion():
    brainwave_data = load_brainwave_data()
    if brainwave_data is None:
        return jsonify({"error": "No brainwave data found"}), 404

    prompt = f"An abstract representation of brainwave patterns: {brainwave_data}"
    image = generate_image(pipe, prompt)

    with NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        image.save(tmp_file.name)
        image_path = tmp_file.name

    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

'''