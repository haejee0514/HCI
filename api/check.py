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

# 첫 번째 API 호출: Explanation 생성
def generate_explanation(prompt):
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
        print(f"Error calling OpenAI API: {e}")
        return None


# 두 번째 API 호출: Image prompt 생성
def generate_image_prompt(explanation):
    try:
        prompt = (
            f"Based on the following explanation of brainwave frequencies: {explanation}, "
            f"generate a prompt to visualize this state as an image."
        )

        response =openai.chat.completions.create(
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
        print(f"Error calling OpenAI API for image prompt: {e}")
        return None


# 뇌파 데이터 처리 함수
def process_brainwave_data(input_data):
    try:
        # 입력 데이터를 바탕으로 explanation을 생성
        prompt = (
            f"My measured brainwaves are as follows: Delta {input_data['Delta']} Hz, "
            f"Theta {input_data['Theta']} Hz, Alpha {input_data['Alpha']} Hz,"
            f"Beta {input_data['Beta']}, Gamma {input_data['Gamma']} Hz.\n"
            "Based on this result, describe the brainwave state in a way that can be visualized as an image."
        )
        print(f"Generated prompt for explanation: {prompt}")  # 디버깅용 로그

        # Explanation 생성
        explanation_result = generate_explanation(prompt)
        if not explanation_result:
            print("Failed to generate explanation.")  # 디버깅용 로그
            return {"status": "error", "message": "Unable to generate explanation", }
        print(f"Generated explanation: {explanation_result}")  # 디버깅용 로그

        # 설명을 바탕으로 image prompt를 생성
        image_prompt_result = generate_image_prompt(explanation_result)
        if not image_prompt_result:
            print("Failed to generate image prompt.")  # 디버깅용 로그
            return {"status": "error", "message": "Unable to generate image prompt"}
        print(f"Generated image prompt: {image_prompt_result}")  # 디버깅용 로그

        return {
            "status": "success",
            "explanation": explanation_result,
            "image_prompt": image_prompt_result
        }
    except Exception as e:
        print(f"Exception in process_brainwave_data: {e}")  # 디버깅용 로그
        return {"status": "error", "message": str(e)}



# 뇌파 데이터 처리 함수
def process_brainwave_data(input_data):
    try:
        # 입력 데이터를 바탕으로 explanation을 생성
        prompt = (
            f"My measured brainwaves are as follows: Delta {input_data['Delta']} Hz, "
            f"Theta {input_data['Theta']} Hz, Alpha {input_data['Alpha']} Hz, "
            f"Beta {input_data['Beta']} Hz, Gamma {input_data['Gamma']} Hz.\n"
            "Based on this result, describe the brainwave state in a way that can be visualized as an image."
        )
        
        # Explanation 생성
        explanation_result = generate_explanation(prompt)
        if not explanation_result:
            error_message = "Failed to generate explanation."
            print(error_message)  # 콘솔 로그
            return {"status": "error", "stage": "explanation", "message": error_message, "input_prompt": prompt}

        # 설명을 바탕으로 image prompt 생성
        image_prompt_result = generate_image_prompt(explanation_result)
        if not image_prompt_result:
            error_message = "Failed to generate image prompt."
            print(error_message)  # 콘솔 로그
            return {
                "status": "error",
                "stage": "image_prompt",
                "message": error_message,
                "explanation_used": explanation_result
            }

        return {
            "status": "success",
            "explanation": explanation_result,
            "image_prompt": image_prompt_result
        }
    except Exception as e:
        error_message = f"Exception in process_brainwave_data: {e}"
        print(error_message)  # 콘솔 로그
        return {"status": "error", "stage": "processing", "message": error_message}


# Flask API 엔드포인트
@brainwaves_bp.route('/api/brainwaves/describe', methods=['POST'])
def process_brainwaves():
    try:
        # JSON 요청에서 뇌파 데이터 가져오기
        input_data = request.get_json()
        print(f"Received input data: {input_data}")  # 콘솔 로그

        # 필수 데이터 확인
        missing_keys = [key for key in ["Delta", "Theta", "Alpha", "Beta", "Gamma"] if key not in input_data]
        if missing_keys:
            error_message = f"Missing required brainwave data: {', '.join(missing_keys)}"
            print(error_message)  # 콘솔 로그
            return jsonify({"status": "error", "stage": "input_validation", "message": error_message}), 400

        # 뇌파 데이터 처리
        result = process_brainwave_data(input_data)
        print(f"Processing result: {result}")  # 콘솔 로그

        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        error_message = f"Exception in processing brainwaves: {e}"
        print(error_message)  # 콘솔 로그
        return jsonify({"status": "error", "stage": "api", "message": error_message}), 500
