# 모듈 설명: AWS 코드 생성 예제 (버전 3)
# - Stability AI를 사용한 이미지 생성 함수입니다.
# - 프롬프트를 받아 이미지를 생성하고 파일로 저장합니다.
# - 주의: 구문 오류 포함 (함수 정의에 콜론 누락)

import base64
import os
import datetime
import re
import requests  # requests 모듈 임포트 추가

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"

# write a python function that takes a prompt and uses stability AI to generate a image and save it to a file

def generate(prompt : str):  # 주의: 원래 코드에 콜론(:) 누락 오류 있음
    # generate image
    response = requests.post(
        f"{api_host}/v1/engines/{engine_id}/generate",
        json={
            "prompt": prompt,
            "num_inference_steps": 50,
            "strength": 0.8,
            "temperature": 0.9,
            "seed": 0,
        },
    )
    # decode image
    image_data = base64.b64decode(response.json()["image"])
    # save image
    filename = f"{prompt.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    with open(filename, "wb") as file:
        file.write(image_data)
    return filename
