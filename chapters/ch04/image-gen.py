# 모듈 설명: OpenAI 이미지 생성 REST API 직접 호출 예제
# - Python 라이브러리 대신 requests로 REST API를 직접 호출합니다.
# - API 키를 파일에서 읽어 Authorization 헤더에 Bearer 토큰으로 사용
#
# 주요 개념:
# - REST API: HTTP POST 요청으로 직접 OpenAI 엔드포인트 호출
# - Bearer Token: API 키를 인증 헤더에 포함시키는 표준 방식
# - 직접 호출의 장점: 더 세밀한 제어, 다른 언어로 쉽게 변환 가능

import requests
import json
import os
import openai
import datetime

# function to read the key
# 로컬 파일에서 API 키를 읽는 함수
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Download and save image
# 생성된 이미지를 다운로드하여 로컬 파일로 저장
def save_image(image_url: str):
    # URL에서 이미지를 요청하고 바이트로 저장
    image_response = requests.get(image_url)
    # 타임스탬프를 포함한 파일명
    filename = f"dalle_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with open(filename, "wb") as f:
        f.write(image_response.content)

# Setup the OpenAI API key and organization
# API 키와 조직 설정
api_key_file = 'OPENAI_API_BOOK_KEY.key'
openai.organization = "org-rocrupyvzgcl4yf25rqq6d1v"
api_key = read_api_key(api_key_file)

# API endpoint URL
# OpenAI 이미지 생성 엔드포인트
url = "https://api.openai.com/v1/images/generations"

# Prompt text
prompt = "laughing panda"

# Request headers
# Authorization 헤더에 Bearer 토큰 포함
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"  # API 키를 Bearer 토큰으로 전달
}

# Request body
# 요청 본문 (JSON 형식)
data = {
    "prompt": prompt,  # 이미지 설명
    "num_images": 2,  # 생성할 이미지 개수 (DALL-E 2: 최대 10)
    "size": "1024x1024"  # 이미지 크기
}

# Make API request
# POST 요청으로 이미지 생성 API 호출
response = requests.post(url, headers=headers, data=json.dumps(data))

# Parse response JSON
# 응답 JSON 파싱
response_data = response.json()
# 예: response_data["data"][0]["url"] 에 이미지 URL이 포함됨
image_url = response_data["data"][0]["url"]
print(response_data)
