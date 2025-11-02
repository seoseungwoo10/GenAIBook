# 모듈 설명: Azure OpenAI 이미지 편집 API 예제
# - Azure OpenAI의 DALL-E 모델을 사용하여 이미지를 생성합니다.
# - 프롬프트를 기반으로 1024x1024 크기의 이미지 생성 및 저장
#
# 주요 개념:
# - DALL-E: OpenAI의 텍스트-to-이미지 생성 모델
# - Image Generation: 자연어 설명으로부터 이미지 생성
# - API Type: 'open_ai' 또는 'azure' 선택 가능

import os
import openai
import requests
import json
import datetime
import re

# OpenAI API 설정
openai.api_type="open_ai"                                   # API 타입 설정
openai.api_key = os.getenv("OPENAI_API_BOOK_KEY")           # 환경변수에서 키 로드
openai.organization = os.getenv("OPENAI_API_BOOK_ORG")      # 조직 ID

# 이미지 생성 파라미터
image_count = 1                                             # 생성할 이미지 개수
image_size = "1024x1024"                                    # 이미지 크기 (256x256, 512x512, 1024x1024)
prompt = "a pineapple that's made of rainbow cake inside, food photography style"  # 이미지 설명

# Set the directory where we'll store the image
# 이미지 저장 디렉터리 설정 및 생성
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
# 파일명에서 특수문자 제거하는 함수
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()  # 허용된 문자만 남기기
    return re.sub(r'[\s]+', '_', s)  # 공백을 언더스코어로 변환

# 이미지 다운로드 및 저장 함수
def save_image(image_url: str):
    image_response = requests.get(image_url)  # URL에서 이미지 다운로드
    # 타임스탬프를 포함한 파일명 생성
    filename = f"{valid_filename(prompt)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    # 바이너리 모드로 이미지 저장
    with open(image_path, "wb") as f:
        f.write(image_response.content)

# 이미지 생성 함수
def generate_images(prompt_startphrase: str):
    # DALL-E API 호출 (구 버전 스타일)
    response = openai.Image.create(
        prompt=prompt_startphrase,  # 이미지 설명
        n=image_count,  # 생성할 이미지 개수
        size=image_size  # 이미지 크기
    )
    return response

# 이미지 생성 및 저장 실행
response = generate_images(prompt)
image_url = response['data'][0]['url']  # 생성된 이미지 URL 추출
save_image(image_url)  # 이미지 다운로드 및 저장
