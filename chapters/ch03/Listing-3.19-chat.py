# 모듈 설명: Listing 3.19 - Chat Completions API 기본 사용 예제
# - Chat API는 대화형 메시지 배열을 사용하여 더 자연스러운 대화를 구현합니다.
# - 각 메시지는 role(system/user/assistant)과 content로 구성됩니다.
# - 대화 기록을 모두 포함시켜야 맥락이 유지됨
#
# 주요 개념:
# - Chat Completions API: 대화형 모델(GPT-3.5, GPT-4)에 최적화된 API
# - Messages: 대화 기록을 나타내는 메시지 배열
# - System Role: 모델의 행동/페르소나 정의 (항상 첫 번째)
# - User Role: 사용자 입력
# - Assistant Role: AI의 이전 응답 (맥락 유지용)

import os
from openai import AzureOpenAI

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"

# Chat Completions API 호출
# messages: 대화 기록을 시간 순서대로 배열
response = client.chat.completions.create(
    model=GPT_MODEL,
    messages = [
        # System 메시지: AI의 역할과 행동 지침 설정
        {"role":"system","content":"You are an AI assistant that helps people find information."},

        # 첫 번째 대화
        {"role":"user","content":"Hello world"},
        {"role":"assistant","content":"Hello! How can I assist you today?"},

        # 두 번째 질문 (이전 대화 맥락이 유지됨)
        {"role":"user","content":"I want to know more about pets and why dogs are good for humans?"}
    ],
    temperature=0.8,       # 창의성 수준
    max_tokens=800,        # 최대 응답 길이
    top_p=0.95,           # 누적 확률 (nucleus sampling)
    frequency_penalty=0,   # 반복 단어 억제 (-2.0 ~ 2.0)
    presence_penalty=0,    # 새로운 주제 도입 장려 (-2.0 ~ 2.0)
    stop=None             # 생성 중단 시퀀스
)

# 모델의 응답 메시지 출력
# response.choices[0].message.content에 답변 텍스트가 포함됨
print(response.choices[0].message.content)
