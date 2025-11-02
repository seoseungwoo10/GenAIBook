# 모듈 설명: Listing 9.6 - Fine-tuning 작업 시작
# - 업로드된 학습 데이터를 사용하여 모델 Fine-tuning 작업을 시작합니다.
# - Hyperparameters를 설정하여 학습 과정을 제어합니다.
#
# 주요 개념:
# - n_epochs: 전체 데이터셋을 몇 번 반복 학습할지 지정 (기본값: 3-4)
# - suffix: Fine-tuning된 모델의 이름에 추가될 접미사
# - model: 기반이 되는 모델 (gpt-35-turbo-0613 등)

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# Begin fine-tuning
# Training file ID: file-0678a7e63fca41a092cffcc473931da2
# Training file name: emoji_FT_train.jsonl

# Fine-tuning 작업 생성 및 시작
ft = client.fine_tuning.jobs.create(
    training_file="file-0678a7e63fca41a092cffcc473931da2",  # 이전에 업로드한 파일 ID
    model="gpt-35-turbo-0613",  # 기반 모델
    hyperparameters={
        "n_epochs":3  # Epoch 수: 데이터셋을 3번 반복 학습
    },
    suffix="emoji"  # 모델 이름 접미사 (예: gpt-35-turbo-emoji)
)
print("Finetuning job ID:", ft.id)  # 작업 추적에 사용할 고유 ID

# Output:
# Finetuning job ID: ftjob-bfaadc862e2c4e66834925fbb645ba80

# List all the FT jobs
# 모든 Fine-tuning 작업 목록 조회
ft_jobs = client.fine_tuning.jobs.list()

for ft_job in ft_jobs:
    # 각 작업의 ID와 현재 상태 출력
    # 상태: pending(대기중), running(실행중), succeeded(성공), failed(실패)
    print(ft_job.id, ft_job.status)

# Output:
# ftjob-bfaadc862e2c4e66834925fbb645ba80 pending
# ftjob-367ee1995af740a0bf24876221585f7a succeeded
# ftjob-c41a9dc551834a1aa0be8befe788a22b succeeded
# ftjob-1a7faac8856d46e48a038c02555fe6e5 succeeded
# ftjob-505d5a8bd321406dbf4605b636b0c0cd succeeded
