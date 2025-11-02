# 모듈 설명: Listing 3.14 - Logit Bias를 사용한 토큰 억제 예제
# - logit_bias 파라미터를 사용하여 특정 토큰의 생성 확률을 조정합니다.
# - -100 값은 해당 토큰이 생성되지 않도록 완전히 억제합니다.
# - 비즈니스 이름 생성 시 특정 단어를 제외하고 싶을 때 유용합니다.

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# logit_bias: 특정 토큰 ID에 대해 -100 ~ 100 사이의 바이어스 적용
# -100은 해당 토큰이 절대 생성되지 않도록 억제
# 100은 해당 토큰의 생성 확률을 극대화
response = client.completions.create(
    model=GPT_MODEL,  
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    logit_bias={
        30026:-100,  # 특정 단어/토큰을 억제
        81:-100,
        9330:-100,
        808:-100,
        42114:-100,
        1308:-100, 
        3808:-100,
        502:-100,
        322:-100}
    )  
  
responsetext = response.choices[0].text
print(responsetext)