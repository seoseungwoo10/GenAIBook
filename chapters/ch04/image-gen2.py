# 모듈 설명: image-gen2
# - openai 라이브러리(Image API)를 사용해 이미지를 생성하고 로컬에 저장합니다.
# - 이미지 저장 디렉터리 생성, 이미지 다운로드/저장 함수 포함.

import os
import openai
import requests
import json
import datetime

openai.api_key = "sk-...."
openai.organization = "org-...."

image_count = 1
image_size = "1024x1024"
prompt = "Laughing panda"


# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')
# If the directory doesn't exist, create it
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)


# Download and save image
def save_image(image_url: str):
    # 이미지 URL에서 콘텐츠를 가져와 파일로 저장
    image_response = requests.get(image_url)
    filename = f"dalle_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image_response.content)
            
def generate_images(prompt_startphrase: str):
    # openai.Image.create를 호출하여 이미지 생성
    response = openai.Image.create(
        prompt=prompt_startphrase,
        n=image_count,
        size=image_size
    )
    return response

response = generate_images(prompt)
image_url = response['data'][0]['url']
save_image(image_url)
