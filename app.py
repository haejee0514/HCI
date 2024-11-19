from flask import Flask
from api.images import images_bp
from api.brainwaves import brainwaves_bp
from api.connect import connect_bp

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 오는 요청 허용

# 블루프린트 등록
app.register_blueprint(connect_bp)
app.register_blueprint(brainwaves_bp)
app.register_blueprint(images_bp)



if __name__ == '__main__':
    app.run(debug=True)
