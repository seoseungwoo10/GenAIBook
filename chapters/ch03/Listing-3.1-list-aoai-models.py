# 모듈 설명: Listing 3.1 - Azure OpenAI에서 사용 가능한 모델 목록 조회
# - AzureOpenAI 클라이언트를 사용해 배포된 모델의 ID, 상태, 기능을 조회하고
#   결과를 JSON 파일로 저장합니다.
# - 환경 변수 AOAI_ENDPOINT와 AOAI_KEY 필요

import os
from openai import AzureOpenAI
import json

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2023-05-15",
    api_key=os.getenv("AOAI_KEY")
    )

# Call the models API to retrieve a list of available models
models = client.models.list()

# save to file
# Convert each Model object in models to a dictionary before serializing it to JSON.
with open('azure-oai-models.json', 'w') as file:
    models_dict = [model.__dict__ for model in models]
    json.dump(models_dict, file)
    
# Print out the names of all the available models, and their capabilities
# 각 모델의 ID, 현재 상태, 기능 출력
for model in models:
    print("ID:", model.id)
    print("Current status:", model.lifecycle_status)
    print("Model capabilities:", model.capabilities)
    print("-------------------")