# 모듈 설명: DALL-E 3를 사용한 이미지 생성 예제 (최신 방식)
# - OpenAI의 최신 Python 클라이언트를 사용하여 DALL-E 3 모델로 이미지 생성
# - natural 스타일과 standard 품질로 고품질 이미지 생성
#
# 주요 개념:
# - DALL-E 3: 가장 최신 버전의 이미지 생성 모델 (품질, 정확도 향상)
# - Style: 'natural' (사실적) 또는 'vivid' (선명하고 과장된)
# - Quality: 'standard' (기본) 또는 'hd' (고해상도, 비용 2배)
# - 새로운 클라이언트 API: client.images.generate() 사용

import os
import openai
import requests
import json
import datetime
import re

from openai import OpenAI

# OpenAI 클라이언트 초기화 (새 방식)
client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# Set the prompt and other parameters
# 이미지 생성 파라미터
image_count = 1
image_size = "1024x1024"  # DALL-E 3: 1024x1024, 1792x1024, 1024x1792
prompt = "a pineapple that's made of rainbow cake inside, food photography style"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

# Function to save the image
def save_image(image_url: str):
    image_response = requests.get(image_url)
    filename = f"{valid_filename(prompt)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image_response.content)

# Function to generate the image
# DALL-E 3를 사용한 이미지 생성 함수
def generate_images(prompt_startphrase: str):
    # 새로운 클라이언트 API 사용
    response = client.images.generate(
        prompt=prompt_startphrase,
        n=image_count,  # DALL-E 3는 n=1만 지원
        model="dall-e-3",  # 모델 지정
        style="natural",  # 스타일: natural 또는 vivid
        quality="standard",  # 품질: standard 또는 hd
        size=image_size)
    return response

# Save the image
# 이미지 생성 및 저장
response = generate_images(prompt)
image_url = response.data[0].url  # 새 API는 .data 속성 사용
save_image(image_url)
