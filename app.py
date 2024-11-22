from flask import Flask
from api.images import images_bp
from api.brainwaves import brainwaves_bp
from api.connect import connect_bp
# from api.ai_status import ai_status_bp
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 블루프린트 등록
app.register_blueprint(connect_bp)
app.register_blueprint(brainwaves_bp)
app.register_blueprint(images_bp)
# app.register_blueprint(ai_status_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

