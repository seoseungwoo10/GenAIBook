# 모듈 설명: Listing 3.6 - 여러 개의 응답 생성 예제
# - n 파라미터를 사용하여 동시에 여러 개의 응답 후보를 생성합니다.
# - n=5로 설정하여 5개의 서로 다른 응답을 받아 선택할 수 있습니다.

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# n=5: 5개의 서로 다른 응답 후보 생성
response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.7,
    max_tokens=100,
    n=5,  # 여러 개의 응답 생성
    stop=None)

# loop through the response choices
# 생성된 모든 응답을 순회하며 출력
for choice in response.choices:
    # print the text of each choice
    print(choice.text)
