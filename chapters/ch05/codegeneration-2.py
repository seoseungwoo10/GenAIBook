# 모듈 설명: 코드 생성 예제 (버전 2)
# - Stability AI를 사용한 이미지 생성 함수의 간단한 구현 예제입니다.
# - base64 인코딩/디코딩을 통한 이미지 데이터 처리 방식 시연

import base64
import os
import requests
import datetime
import re

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"

# write a python function that takes a prompt and uses stability AI to generate a image and save it to a file
def generate(prompt):
    # encode prompt to base64
    prompt = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")

    # get the response from the API
    response = requests.post(f"{api_host}/v1/engines/{engine_id}/completions", json={"prompt": prompt})

    # get the image from the response
    image = response.json()["choices"][0]["text"]

    # decode the image from base64
    image = base64.b64decode(image)

    # save the image to a file
    with open(f"images/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png", "wb") as file:
        file.write(image)
