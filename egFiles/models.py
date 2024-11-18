from diffusers import StableDiffusionPipeline
import torch
from config import MODEL_ID

# Stable Diffusion 모델 초기화
def load_stable_diffusion():
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    return pipe

# 이미지 생성 함수
def generate_image(pipe, prompt):
    image = pipe(prompt).images[0]
    return image