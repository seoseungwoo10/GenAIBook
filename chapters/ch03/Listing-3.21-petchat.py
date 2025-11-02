# 모듈 설명: Listing 3.21 - 간단한 챗봇 예제
# - 대화 기록을 유지하며 연속적인 대화를 가능하게 하는 챗봇입니다.
# - 무한 루프로 사용자 입력을 받고 AI 응답을 생성합니다.

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

# 시스템 프롬프트: 챗봇의 역할 정의
conversation=[{"role": "system", "content": "You are a helpful AI assistant and happy to talk about pets and salons."}]

while True:
    user_input = input()      
    # 사용자 입력을 대화 기록에 추가
    conversation.append({"role": "user", "content": user_input})

    # Chat Completions API 호출
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=conversation
    )

    # AI 응답을 대화 기록에 추가
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")