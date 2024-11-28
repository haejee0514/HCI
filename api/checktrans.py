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
global image_prompt
image_prompt="Visualize a serene scene of a person meditating by a tranquil forest pond, surrounded by nature's sounds and sunlight piercing through the leaves, peacefully soaking their hand in the water, enjoying the calmness and tranquility of the present moment."

def translate_prompt_to_english(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-3.5 Turbo 모델을 사용
            messages=[
                {"role": "system", "content": "Translate the following text to English:"},
                {"role": "user", "content": prompt}
            ],
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


print(combine_prompts_with_openai(image_prompt,"이미지를 기존이랑 유지하되, 더 밝게 바꿔줘"))
