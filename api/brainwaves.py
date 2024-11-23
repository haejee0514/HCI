import openai
import os
import sys
from flask import Flask, request, jsonify, Blueprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests

from stable_diffusion import request_image_generation, API_KEY , seed, request_image_modifying

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
                {"role": "system", "content": (
                    "뇌파에 관한 과학적 배경 정보를 바탕으로 사용자의 상태를 한국어로 설명하고, 어떤 식으로 visualize 할 건지 방향성 제시"
                    "문장은 100 토큰 안에 무조건 끝내도록 해."
                    "각 뇌파는 특정한 상태를 나타낸다:\n"
                    "- Delta (0.5-4Hz): 깊은 수면 상태.\n"
                    "- Theta (4-8Hz): 가벼운 수면, 명상, 깊은 이완.\n"
                    "- Alpha (8-13Hz): 이완, 각성 상태, 스트레스 감소.\n"
                    "- Beta (13-30Hz): 집중력, 논리적 사고, 스트레스 상태.\n"
                    "- Gamma (30-100Hz): 고도의 집중, 문제 해결, 학습.\n"
                )},
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
            f"generate a prompt to visualize this state as an image. End the sentence in 30 tokens."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI artist supporter. Provide an concrete idea for drawing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=30
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
            "이 뇌파로 사용자의 상태를 설명하고, 어떤 식으로 그림을 만들 수 있는지 설명해."
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
    




API_KEY= API_KEY

import requests

base_image=None
seed=None

import base64
# 기존 이미지 생성 엔드포인트
@brainwaves_bp.route('/api/images/generate', methods=['GET'])
def generate_image():
    global base_image
    global image_prompt
    print(image_prompt)
    
    # 이미지 생성 요청
    response = request_image_generation(image_prompt)

    if response.get("status") == "success":
        base_image = response.get("generated_image")
        
        # Base64 문자열을 JSON 응답으로 반환
        return jsonify({
            "status": "success",
            "generated_image": base_image  # Base64 문자열 그대로 반환
        }), 200
    else:
        # 실패한 경우 적절한 오류 응답 반환
        return jsonify(response), 400



additional_prompt=None

# 이미지 수정(Inpainting) 엔드포인트
@brainwaves_bp.route('/api/images/modified', methods=['POST'])
def add_prompt():
    global additional_prompt
    try:
        # 요청 데이터 받기
        data = request.json
        if not data or "inputs" not in data:
            return jsonify({"error": "Invalid input, 'inputs' is required"}), 400

        # 'inputs' 값 처리
        additional_prompt = data.get("inputs")
        
        # 성공 응답
        response = {
            "status": "success",
            "message": "Image modification request received successfully",
            "data": {"additional_prompt": additional_prompt}
        }
        print("Response data:", response)
        return jsonify(response), 200

    except Exception as e:
        # 에러 처리
        error_response = {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
        print("error data:", error_response)
        return jsonify(error_response), 500
    
    
@brainwaves_bp.route('/api/images/regenerate', methods= ['GET'])

def modify_image():
    global seed
    global base_image
    global additional_prompt
    # 이미지를 수정하는 요청을 보냄
    response = request_image_modifying(base_image, additional_prompt)
    return jsonify(response)