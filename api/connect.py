# Muse 2 연결 확인 API

from flask import Flask, jsonify, Blueprint, request

connect_bp = Blueprint('connect',__name__)


muse_connected_status= False  # 초기 상태는 False

@connect_bp.route('/api/brainwaves/connect-status', methods=['POST'])
def update_muse_status():
    global muse_connected_status
    data = request.get_json()

    if 'connected' not in data:
        return jsonify({"status": "error", "message": "Invalid connection status data."}), 400
    
    muse_connected_status = data['connected']
    return jsonify({"status": "success", "message": "Muse 2 connection status updated."}), 200


@connect_bp.route('/api/connect', methods=['GET'])
def get_muse_status():
    global muse_connected_status

    return jsonify({"connected": muse_connected_status}), 200