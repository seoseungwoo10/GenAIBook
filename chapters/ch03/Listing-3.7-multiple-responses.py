# 모듈 설명: Listing 3.7 - best_of 파라미터를 사용한 최적 응답 선택 예제
# - best_of 파라미터를 사용하여 내부적으로 여러 응답을 생성한 후 최상의 결과를 반환합니다.
# - n과 best_of의 차이: n은 모든 응답을 반환, best_of는 최선의 1개만 반환

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# best_of=5: 5개 중에서 가장 좋은 응답 1개 선택
# 내부적으로 5개를 생성하지만 최상의 결과만 반환 (비용은 5개 분량)
response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.7,
    max_tokens=100,
    best_of=5,  # 5개 중 최선의 결과 선택
    #n=5,  # n과 함께 사용 불가
    stop=None)

# loop through the response choices
for choice in response.choices:
    # print the text of each choice
    print(choice.text)
