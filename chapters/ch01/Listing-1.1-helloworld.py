# 모듈 설명: Listing 1.1
# - OpenAI 클라이언트를 사용해 간단한 챗 요청을 보내고
#   응답을 받아 다른 언어로 번역 요청을 하는 예제입니다.
# - 실제로 실행하려면 OpenAI API 키 설정 및 적절한 모델명 사용이 필요합니다.

import os
from openai import OpenAI

# 사용할 GPT 모델 지정
GPT_MODEL = "gpt-3.5-turbo"

# OpenAI API 클라이언트 초기화 (예: 환경변수 또는 하드코딩 키 필요)
client = OpenAI(api_key='your-api-key')

# 영어로 간단한 프롬프트를 보내고 응답을 받아 출력
response_english = client.chat.completions.create(
    model=GPT_MODEL,
    messages=[
      {
        "role": "user",  # 메시지 작성자 역할 (user/system/assistant 등)
        "content": "Hello, World!"
      }
    ],
    max_tokens=50  # 응답에서 허용할 최대 토큰 수
)
# 응답에서 텍스트 부분을 추출하여 출력
english_text = response_english.choices[0].message.content.strip()
print(english_text)

# 영어 응답을 프랑스어로 번역해 달라고 다시 모델에 요청
response_french = client.chat.completions.create(
    model=GPT_MODEL,
    
    messages=[
      {
        "role": "user",
        "content": "Translate the following English text to French: " + english_text
      }
    ],
    max_tokens=100  # 번역 결과에 더 많은 토큰 허용
)
# 번역된 문자열을 출력
print(response_french.choices[0].message.content.strip())
