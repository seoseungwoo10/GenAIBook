# 모듈 설명: Listing 9.7 - Fine-tuning 작업 목록 조회
# - 현재 계정에서 실행한 모든 Fine-tuning 작업의 목록을 확인합니다.
# - 각 작업의 ID와 상태를 통해 진행 상황을 파악할 수 있습니다.
#
# 작업 상태 설명:
# - pending: 대기 중 (큐에 있음)
# - running: 실행 중 (학습 진행 중)
# - succeeded: 성공 (모델 사용 가능)
# - failed: 실패 (오류 발생)
# - cancelled: 취소됨

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# List all the FT jobs
# 모든 Fine-tuning 작업 목록을 조회
ft_jobs = client.fine_tuning.jobs.list()

# 각 작업의 ID와 상태를 출력
for ft_job in ft_jobs:
    print(ft_job.id, ft_job.status)

# Output:
# ftjob-bfaadc862e2c4e66834925fbb645ba80 pending      <- 대기 중
# ftjob-367ee1995af740a0bf24876221585f7a succeeded   <- 완료
# ftjob-c41a9dc551834a1aa0be8befe788a22b succeeded   <- 완료
# ftjob-1a7faac8856d46e48a038c02555fe6e5 succeeded   <- 완료
# ftjob-505d5a8bd321406dbf4605b636b0c0cd succeeded   <- 완료
