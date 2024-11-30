import openai
import os
import sys
from flask import Flask, request, jsonify, Blueprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests

from stable_diffusion import request_image_generation, API_KEY, request_image_modifying

# OpenAI API 키 설정
from config import OPENAI_KEY
openai.api_key = OPENAI_KEY

# Flask 애플리케이션 초기화
brainwaves_bp = Blueprint('brainwaves',__name__)
success=None
explanation=None
image_prompt=None
seed=None
import random


# 첫 번째 API 호출: Explanation 생성
def generate_explanation(prompt):
    global success
    global seed
    seed = random.randint(1, 100000)
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                "content": "각 뇌파 상태는 다양한 감정, 상황, 그리고 환경적 변화를 반영할 수 있습니다. 아래 뇌파 상태에 대해 사용자의 상태를 설명하고, 그 상태에 맞는 시각적 표현 방법을 아이디어만 간단하게 하나만 제시해 주세요. 다음 예시는 그냥 아이디어일 뿐이니 무시해도 됩니다. 색상, 구성, 감정적인 요소를 다양하게 고려하지만, 자세하면 안됩니다. Delta: 어두운 환경, 흐릿한 빛, 혹은 잠자는 사람의 모습을 나타낼 수 있습니다. 이 외에도 꿈 속의 환상적인 풍경, 혹은 평화롭고 고요한 자연 환경 등 다양한 방식으로 표현할 수 있습니다. 또한, 공간이 넓고 어두운 이미지나, 잠에 빠져드는 순간의 감각을 시각적으로 담을 수 있습니다. Theta: 명상, 깊은 이완  명상 상태나 깊은 이완을 상징하는 다양한 시각적 표현을 고려해 주세요. 예를 들어, 잔잔한 자연 풍경, 산속의 명상하는 사람, 혹은 공기처럼 흐르는 추상적인 형태들이 떠오를 수 있습니다. 부드러운 색조와 차분한 분위기 외에도, 더 환상적이거나 꿈같은 이미지를 상상해볼 수 있습니다. 색감은 차분하고 은은한 느낌으로, 상상력을 자극하는 풍경을 그릴 수 있습니다. Alpha: 이완, 각성 상태, 스트레스 감소. 편안하고 차분한 상태를 나타내는 다양한 이미지들. 부드러운 자연 장면, 혹은 공허함을 느낄 수 있는 넓은 공간, 가벼운 구름과 함께 느긋한 분위기를 연출할 수 있습니다. 이 외에도 스트레스를 해소하는 활동을 묘사하는 것도 가능합니다. 예를 들어, 따뜻한 햇살 속에서 이완되는 사람의 모습, 바다와 하늘이 맞닿은 넓은 공간 등을 고려할 수 있습니다. Beta: 집중력과 스트레스가 동시에 발현되는 상태로, 복잡하고 치열한 환경, 또는 격렬한 운동이나 논리적인 문제를 푸는 모습 등을 시각적으로 표현할 수 있습니다. 강렬한 색상, 격자무늬, 빠르게 움직이는 사람의 모습 등도 다양하게 그릴 수 있습니다. 또한, 차가운 색조와 복잡한 기하학적 패턴을 사용하여 집중적인 에너지를 표현할 수 있습니다. Gamma: 매우 높은 집중 상태로, 에너지 넘치는 장면이나 머릿속에서 여러 가지 아이디어가 떠오르는 순간을 그릴 수 있습니다. 매우 다양한 색상과 형상, 빠르게 변화하는 이미지를 고려해 보세요. 무언가를 해결하려는 행동이나 창의적인 아이디어가 현실로 나타나는 장면 등도 가능성이 있습니다. 빛이 반짝이는 순간, 여러 가지 요소들이 빠르게 떠오르는 모습 등을 시각화할 수 있습니다."
                },
                {"role": "user", "content": prompt}
            ]
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
                {"role": "system", "content": "You are an AI artist supporter. Provide an concrete idea for drawing in 2 sentences"},
                {"role": "user", "content": prompt}
            ]
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
            "Explain user's condition with this brainwave, and explain how you can make a picture in korean and it should be short."
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
    


#    주어진 이미지 재생성 프롬프트를 OpenAI를 사용하여 영어로 번역하는 함수.
def translate_prompt_to_english(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-3.5 Turbo 모델을 사용
            messages=[
                {"role": "system", "content": "Translate the following text to English:"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        translated_prompt = response.choices[0].message.content.strip()
        print(f"Translated Prompt: {translated_prompt}")  # 번역된 프롬프트 출력
        return translated_prompt
    except Exception as e:
        print(f"Error in translation: {e}")  # 번역 중 발생한 오류 출력
        return None




def combine_prompts_with_openai(image_prompt, translated_prompt):
    try:
        # OpenAI API를 사용하여 두 텍스트를 자연스럽게 결합하도록 요청
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-3.5 Turbo 모델을 사용
            messages=[
                {"role": "system", "content": "You are an AI assistant that combines descriptions to create a more complete and coherent prompt."},
                {
                    "role": "user",
                    "content": f"Use the following description as a base for the image: {image_prompt}. Now, apply the following modification to the image: {translated_prompt}. Provide a detailed and coherent description combining both, ensuring the original vision is preserved while applying the change in 3 sentences"
                }
            ],
        )

        # 모델의 응답에서 결합된 텍스트 추출
        combined_prompt = response.choices[0].message.content.strip()
        print(f"Combined Prompt: {combined_prompt}")  # 결합된 프롬프트 출력

        return combined_prompt

    except Exception as e:
        print(f"Error in combining prompts: {e}")  # 오류 발생 시 출력
        return None




API_KEY= API_KEY

import requests

base_image=None

import base64
# 기존 이미지 생성 엔드포인트
@brainwaves_bp.route('/api/images/generate', methods=['GET'])
def generate_image():
    global base_image
    global image_prompt
    global seed
    print(image_prompt, seed)
    
    # 이미지 생성 요청
    response = request_image_generation(image_prompt,seed)

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
    global base_image
    global additional_prompt
    global seed
    global image_prompt
    print(seed)
    translated_prompt = translate_prompt_to_english(additional_prompt)
    # 이미지를 수정하는 요청을 보냄
    combined_prompt=combine_prompts_with_openai(image_prompt,translated_prompt)
    response = request_image_modifying(base_image, combined_prompt ,seed)
    return jsonify(response)