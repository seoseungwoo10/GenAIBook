# 모듈 설명: OpenAI Completion을 사용한 간단한 예제
# - Azure OpenAI(또는 OpenAI) 환경에서 Completion API를 호출하여
#   프롬프트에 대한 텍스트 응답을 얻고 출력합니다.
# - 실제 실행 시에는 AOAI_ENDPOINT와 AOAI_KEY 환경 변수가 필요합니다.

import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

prompt_startphrase = "Suggest three names for a new pet salon business."

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt_startphrase,
  temperature=0.8,
  max_tokens=100,
  suffix="\nThats all folks!",
  stop=None)

responsetext = response["choices"][0]["text"]

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

print(response)
