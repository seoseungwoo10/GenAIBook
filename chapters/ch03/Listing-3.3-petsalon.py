# 모듈 설명: Listing 3.3 - 펫 살롱 이름 제안 예제 (다중 응답)
# - Azure OpenAI Completion API의 n 파라미터를 사용하여 여러 개의 응답 후보를 생성합니다.
# - n=3: 동시에 3개의 서로 다른 응답을 생성하여 선택의 폭을 넓힘
#
# 주요 개념:
# - n 파라미터: 한 번의 API 호출로 여러 응답 생성 (비용은 n배)
# - temperature=0.7: 적절한 창의성과 일관성의 균형
# - Completion API: 프롬프트를 완성하는 형태의 텍스트 생성

import os
from openai import AzureOpenAI

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

# 비즈니스 이름 생성을 위한 프롬프트
# 원하는 특성(전문적, 친근함, 개인화)을 명시하여 관련성 높은 결과 유도
prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# Completion API 호출
# n=3: 3개의 서로 다른 응답 후보 생성
# 각 응답은 response.choices 리스트에 저장됨
response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.7,  # 창의성 수준 (0-2, 높을수록 다양하지만 일관성 낮음)
    max_tokens=100,   # 생성할 최대 토큰 수
    #best_of=5,  # 옵션: 5개 중 최선 1개 선택 (n과 함께 사용 불가)
    n=3,  # 3개의 응답 후보 생성
    stop=None)  # 생성 중단 시퀀스 (없음)

# 첫 번째 응답 출력 (나머지는 response.choices[1], [2]로 접근 가능)
responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
