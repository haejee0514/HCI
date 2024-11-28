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


print(translate_prompt_to_english("이미지를 기존이랑 유지하되, 더 밝게 바꿔줘"))
