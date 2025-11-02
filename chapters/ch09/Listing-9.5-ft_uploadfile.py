# 모듈 설명: Listing 9.5 - Fine-tuning 학습 파일 업로드
# - Azure OpenAI의 Fine-tuning API를 사용하여 학습 데이터 파일을 업로드합니다.
# - 업로드된 파일은 Fine-tuning 작업에서 사용할 수 있는 고유 ID를 받습니다.
#
# Fine-tuning이란?
# - 기존 LLM을 특정 도메인이나 태스크에 맞게 추가 학습시키는 과정
# - 소량의 데이터로도 모델의 성능을 특정 용도에 맞게 개선 가능
# - 일관된 출력 형식, 특정 톤/스타일, 도메인 지식 강화 등에 활용

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

# Azure OpenAI 클라이언트 초기화
# Fine-tuning을 위한 별도의 엔드포인트와 키 사용
client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

TRAINING_FILENAME = 'data/emoji_FT_train.jsonl'
#validation_file_name = 'data/validation_set.jsonl'

# Upload the training and validation dataset files to Azure OpenAI with the SDK.
# 학습 데이터셋 파일을 Azure OpenAI에 업로드
# purpose="fine-tune": 이 파일이 Fine-tuning 용도임을 명시
file = client.files.create(
    file=open(TRAINING_FILENAME, "rb"),
    purpose="fine-tune"
)

print("Training file ID:", file.id)  # Fine-tuning 작업에서 사용할 파일 ID
print("Training file name:", file.filename)
