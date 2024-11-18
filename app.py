from flask import Flask, request, jsonify

from stable_diffusion import request_image_generation
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
