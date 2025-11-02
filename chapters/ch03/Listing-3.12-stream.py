# 모듈 설명: Listing 3.12 - 스트리밍 방식의 Completion 예제
# - stream=True 파라미터를 사용하여 생성되는 텍스트를 실시간으로 받아옵니다.
# - 긴 응답을 생성할 때 사용자에게 즉각적인 피드백 제공 가능
# - ChatGPT와 같은 타이핑 효과 구현에 사용
#
# 주요 개념:
# - Streaming: 전체 응답을 기다리지 않고 생성되는 대로 받음
# - Server-Sent Events (SSE): 스트리밍의 기반 기술
# - sys.stdout.flush(): 버퍼링 없이 즉시 출력
# - 장점: 사용자 경험 향상, 응답 시작 시간 단축

import os
import sys
from openai import AzureOpenAI

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"

# 복잡한 요청 프롬프트 (이름 3개 + 3문장 이상의 태그라인)
prompt_startphrase = "Suggest three names and a tagline which is at least 3 sentences for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# stream=True: 응답을 실시간 스트리밍으로 받음
# for 루프로 각 응답 청크(chunk)를 순회
for response in client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=500,
    n=1,
    stream=True,  # 스트리밍 활성화
    stop=None):

    # 각 청크의 텍스트를 즉시 출력
    # response.choices에는 생성된 텍스트 조각이 포함됨
    for choice in response.choices:
        # 버퍼링 없이 즉시 출력 (타이핑 효과)
        sys.stdout.write(str(choice.text)+"\n")
        sys.stdout.flush()  # 버퍼 강제 플러시
