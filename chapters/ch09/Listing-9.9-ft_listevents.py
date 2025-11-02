# 모듈 설명: Listing 9.9 - Fine-tuning 작업의 이벤트 로그 조회
# - 특정 Fine-tuning 작업의 상세 이벤트를 확인합니다.
# - 학습 진행 상황, 검증 손실(validation loss), 에러 메시지 등을 확인할 수 있습니다.
#
# 이벤트 로그 활용:
# - 학습 진행률 확인
# - 문제 발생 시 원인 파악
# - 모델 성능 지표 모니터링 (loss, accuracy 등)

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# List all the FT events for the job from earlier - ftjob-bfaadc862e2c4e66834925fbb645ba80
# 특정 Fine-tuning 작업의 이벤트 로그 조회
# limit=10: 최근 10개의 이벤트만 가져오기
ft_job_events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id="ftjob-bfaadc862e2c4e66834925fbb645ba80", 
    limit=10)

# Loop through the events and print the details
# 각 이벤트의 ID와 메시지를 출력
# 메시지 예: "Step 100: training loss=0.45", "Job completed successfully" 등
for ft_job_event in ft_job_events:
    print(ft_job_event.id, ft_job_event.message)