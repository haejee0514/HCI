import openai
import os
import sys
from flask import Flask, request, jsonify, Blueprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# OpenAI API 키 설정
from config import OPENAI_KEY
openai.api_key = OPENAI_KEY

# Flask 애플리케이션 초기화
brainwaves_bp = Blueprint('brainwaves',__name__)
success=None
explanation=None
image_prompt=None

# 첫 번째 API 호출: Explanation 생성
def generate_explanation(prompt):
    global success
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        success = "error"
        print(f"Error calling OpenAI API: {e}")
        return None


# 두 번째 API 호출: Image prompt 생성
def generate_image_prompt(explanation):
    global success
    try:
        prompt = (
            f"Based on the following explanation of brainwave frequencies: {explanation}, "
            f"generate a prompt to visualize this state as an image."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI artist supporter. Provide an idea for drawing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=70
        )

        image_prompt = response.choices[0].message.content.strip()
        return image_prompt

    except Exception as e:
        success = "error"
        print(f"Error calling OpenAI API for image prompt: {e}")
        return None


# 뇌파 데이터 처리 함수
def process_brainwave_data(input_data):
    global success
    try:
        # 입력 데이터를 바탕으로 explanation 생성
        prompt = (
            f"My measured brainwaves are as follows: Delta {input_data['Delta']} Hz, "
            f"Theta {input_data['Theta']} Hz, Alpha {input_data['Alpha']} Hz, "
            f"Beta {input_data['Beta']} Hz, Gamma {input_data['Gamma']} Hz.\n"
            "Based on this result, describe the brainwave state in a way that can be visualized as an image."
        )

        # Explanation 생성
        explanation_result = generate_explanation(prompt)
        if not explanation_result:
            success = "error"
            error_message = "Failed to generate explanation."
            print(error_message)
            return {"status": "error", "stage": "explanation", "message": error_message, "input_prompt": prompt}

        # 설명을 바탕으로 image prompt 생성
        image_prompt_result = generate_image_prompt(explanation_result)
        if not image_prompt_result:
            success = "error"
            error_message = "Failed to generate image prompt."
            print(error_message)
            return {
                "status": "error",
                "stage": "image_prompt",
                "message": error_message,
                "explanation_used": explanation_result
            }

        success = "started"  # 성공적으로 데이터 처리 완료
        return {
            "status": "success",
            "explanation": explanation_result,
            "image_prompt": image_prompt_result
        }
    except Exception as e:
        success = "error"
        error_message = f"Exception in process_brainwave_data: {e}"
        print(error_message)
        return {"status": "error", "stage": "processing", "message": error_message}


# Flask API 엔드포인트
@brainwaves_bp.route('/api/brainwaves/describe', methods=['POST'])
def process_brainwaves():
    global success
    global explanation
    global image_prompt
    try:
        success = "pending"  # 요청 처리 시작
        # JSON 요청에서 뇌파 데이터 가져오기
        input_data = request.get_json()
        print(f"Received input data: {input_data}")

        # 필수 데이터 확인
        missing_keys = [key for key in ["Delta", "Theta", "Alpha", "Beta", "Gamma"] if key not in input_data]
        if missing_keys:
            success = "error"
            error_message = f"Missing required brainwave data: {', '.join(missing_keys)}"
            print(error_message)
            return jsonify({"status": "error", "stage": "input_validation", "message": error_message}), 400

        # 뇌파 데이터 처리
        result = process_brainwave_data(input_data)
        print(f"Processing result: {result}")

        if result["status"] == "success":
            success = "started"
            explanation=result["explanation"]
            image_prompt=result["image_prompt"]
            return jsonify(result), 200
        else:
            success = "error"
            return jsonify(result), 500 
    except Exception as e:
        success = "error"
        error_message = f"Exception in processing brainwaves: {e}"
        print(error_message)
        return jsonify({"status": "error", "stage": "api", "message": error_message}), 500



@brainwaves_bp.route('/api/ai-status', methods=['GET'])
def get_ai_status():
    global success
    try:
        # Determine the message based on the status
        if success == "started":
            message = "AI 이미지 생성이 시작되었습니다."
        elif success == "pending":
            message = "AI 이미지 생성 대기 중입니다."
        else:
            message = "이미지 생성 상태를 확인하는 중 오류가 발생했습니다."
        
        # Return the status and the dynamically generated message
        return jsonify({
            "status": success,
            "message": message
        }), 200
    except Exception as e:
        # Handle unexpected server errors
        return jsonify({
            "status": "error",
            "message": "이미지 생성 상태를 확인하는 중 오류가 발생했습니다."
        }), 500
    


@brainwaves_bp.route('/api/get-description', methods=['GET'])
def get_description():
    global explanation  # '설명' 데이터가 여기에 저장된다고 가정
    global success      # 'status' 정보를 저장한다고 가정
    
    try:
        if not explanation:  # 설명 데이터가 없을 경우 404 반환
            return jsonify({
                "status": "error",
                "message": "No description available.!!"
            }), 404
        
        # 성공 상태에 따른 설명 반환
        if success == "started":
            status="success"
        else:
            status="error"
            message="No description available.!"
        
        return jsonify({
            "status": "success",
            "explanation": explanation
        }), 200
    
    except Exception as e:
        # 서버 에러 발생 시 500 반환
        return jsonify({
            "status": "error",
            "message": "Internal server error occurred."
        }), 500