from flask import Blueprint, jsonify

# Create a Blueprint for AI status
ai_status_bp = Blueprint('ai-status', __name__)

# Example of AI status
AI_STATUS = {
    "status": "started"  # Possible values: "started", "pending", "error"
}

@ai_status_bp.route('/api/ai-status', methods=['GET'])
def get_ai_status():
    try:
        # Determine the message based on the status
        if AI_STATUS["status"] == "started":
            message = "AI 이미지 생성이 시작되었습니다."
        elif AI_STATUS["status"] == "pending":
            message = "AI 이미지 생성 대기 중입니다."
        else:
            # Handle unexpected or invalid statuses
            raise ValueError("Invalid status")
        
        # Return the status and the dynamically generated message
        return jsonify({
            "status": AI_STATUS["status"],
            "message": message
        }), 200
    except Exception as e:
        # Handle unexpected server errors
        return jsonify({
            "status": "error",
            "message": "이미지 생성 상태를 확인하는 중 오류가 발생했습니다."
        }), 500
