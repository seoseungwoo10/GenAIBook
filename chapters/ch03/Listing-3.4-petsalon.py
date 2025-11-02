# 모듈 설명: Listing 3.4 - 펫 살롱 이름 제안 예제 (단순 버전)
# - Azure OpenAI Completion API를 사용하여 비즈니스 이름을 생성합니다.
# - temperature=0.7로 설정하여 적절한 창의성과 일관성의 균형 유지

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# Completion API 호출 (단일 응답 생성)
response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.7,
    max_tokens=100,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
