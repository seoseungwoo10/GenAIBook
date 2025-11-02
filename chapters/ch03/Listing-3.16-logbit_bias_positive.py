# 모듈 설명: Listing 3.16 - Logit Bias를 사용한 긍정적 바이어스 예제
# - logit_bias에 양수 값을 사용하여 특정 토큰의 생성 확률을 높입니다.
# - 음수(-100)로 원하지 않는 단어를 억제하고, 양수(5)로 원하는 단어를 장려합니다.

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"
  
prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

# logit_bias: 음수로 억제, 양수로 장려
response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    logit_bias={
        30026:-100,  # 특정 토큰 억제
        81:-100,
        9330:-100,
        808:-100,
        42114:-100,
        1308:-100, 
        3808:-100,
        502:-100,
        322:-100,
        37:5,      # 특정 토큰 장려 (양수 바이어스)
        16682:5
    }
)
  
responsetext = response.choices[0].text
print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
