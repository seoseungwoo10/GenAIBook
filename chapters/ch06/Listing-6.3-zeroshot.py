# 모듈 설명: Listing 6.3 - Zero-shot 학습 예제
# - 별도의 예제 없이 단순한 지시만으로 번역 작업 수행
# - Few-shot과 비교하여 모델의 기본 능력에 의존

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY")
)

GPT_MODEL = "gpt-35-turbo"

# Zero-shot 프롬프트: 예제 없이 직접 작업 지시
prompt_startphrase = "Translate the following to Spanish: I have a small dog called Champ."

response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
