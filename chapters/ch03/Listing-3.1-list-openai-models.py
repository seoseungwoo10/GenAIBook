# 모듈 설명: Listing 3.1 - 조직에 사용 가능한 OpenAI 모델 목록 조회 예제
# - 로컬 파일에 저장된 API 키를 읽어 OpenAI 클라이언트를 초기화하고 모델 목록을 가져옵니다.
# - 결과는 콘솔에 출력되고 `oai-models.json`에 저장됩니다.

# Variant of Listing 3.1 - list models available in OpenAI for the current organization

import os
import openai
from openai import OpenAI

api_key_file = '../../OPENAI_API_BOOK_KEY.key'

# function to read the key
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=read_api_key(api_key_file))

# Call the models API to retrieve a list of available models
models = client.models.list()

# save to file (문자열로 저장 — 필요 시 json 모듈로 포맷 가능)
with open('oai-models.json', 'w') as file:
    file.write(str(models))

# Print out basic 정보
for model in models.data:
    print("ID:", model.id)
    print("Model owned by:", model.owned_by)
    print("-------------------")