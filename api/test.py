import openai
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# OpenAI API 키 설정
from config import OPENAI_KEY
openai.api_key = OPENAI_KEY


# 첫 번째 API 호출: Explanation 생성
def explanation(prompt):
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
        print(f"Explanation response: {explanation}")  # 디버깅을 위한 출력
        return explanation
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


# 두 번째 API 호출: Image prompt 생성
def image_prompt(explanation):
    try:
        prompt = (
            f"Based on the following explanation of brainwave frequencies: {explanation}, "
            f"generate a prompt to visualize this state as an image."
        )
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[ 
                {"role": "system", "content": "You are an AI artist. Provide idea for drawing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=70
        )

        image_prompt = response.choices[0].message.content.strip()
        print(f"Image prompt response: {image_prompt}")  # 디버깅을 위한 출력
        return image_prompt
    
    except Exception as e:
        print(f"Error calling OpenAI API for image prompt: {e}")
        return None


# 뇌파 데이터 처리 함수
def process_brainwave_data(input_data):
    # 입력 데이터를 바탕으로 explanation을 생성
    prompt = (
        f"My measured brainwaves are as follows: Delta {input_data['Delta']} Hz, "
        f"Theta {input_data['Theta']} Hz, Alpha {input_data['Alpha']} Hz, "
        f"Beta{input_data['Beta']} Hz, Gamma {input_data['Gamma']} Hz.\n"
        "Based on this result, describe the brainwave state in a way that can be visualized as an image."
    )
    
    # Explanation 생성
    explanation_result = explanation(prompt)
    if not explanation_result:
        return {"status": "error", "message": "Unable to generate explanation"}
    
    # 설명을 바탕으로 image prompt를 생성
    image_prompt_result = image_prompt(explanation_result)
    if not image_prompt_result:
        return {"status": "error", "message": "Unable to generate image prompt"}
    
    return {
        "status": "success",
        "explanation": explanation_result,
        "image_prompt": image_prompt_result
    }

# 로컬 데이터 테스트
if __name__ == "__main__":
    input_data = {
        "Delta": 0.1,
        "Theta": 0.2,
        "Alpha": 0.5,
        "Beta":0.1,
        "Gamma": 0.2
    }
    
    result = process_brainwave_data(input_data)
    
    if result["status"] == "success":
        print("Explanation:", result["explanation"])
        print("Image Prompt:", result["image_prompt"])
    else:
        print("Error:", result["message"])
