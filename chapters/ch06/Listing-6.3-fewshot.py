# 모듈 설명: Listing 6.3 - Few-shot 학습 예제
# - 프롬프트에 여러 개의 Definition + Example 쌍을 제공하여
#   모델이 패턴을 학습하고 새로운 예제를 생성하도록 유도합니다.
# - 가상의 단어(whatpu, farduddle, yalubalu)를 사용한 창의적 예제

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY")
)

GPT_MODEL = "gpt-35-turbo"

# Few-shot 프롬프트: 정의와 예제를 여러 번 제공
prompt_startphrase = "Definition: A \"whatpu\" is a small, furry animal native to Tanzania. \nExample: We were traveling in Africa and we saw these very cute whatpus.\n\nDefinition: To do a \"farduddle\" means to jump up and down really fast. \nExample: One day when I was playing tag with my little sister, she got really excited and she started doing these crazy farduddles.\n\nDefinition: A \"yalubalu\" is a type of vegetable that looks like a big pumpkin. \nExample:"

response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
