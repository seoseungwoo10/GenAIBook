# 모듈 설명: Listing 9.10 - Fine-tuning 작업 상태 폴링(Polling)
# - Fine-tuning 작업이 완료될 때까지 주기적으로 상태를 확인합니다.
# - 작업 완료까지 30초마다 상태를 체크하고 경과 시간을 표시합니다.
#
# 폴링(Polling)이란?
# - 특정 작업의 상태를 주기적으로 확인하는 방식
# - Fine-tuning은 시간이 오래 걸리므로(수 시간) 폴링으로 모니터링
# - 완료 상태(succeeded/failed)가 될 때까지 반복 확인

import os
import time
from openai import AzureOpenAI
from IPython.display import clear_output

# Define the API version
API_VERSION = '2023-09-15-preview'

# Create an instance of the AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# Define the job ID of the fine-tuning job to track
# 모니터링할 Fine-tuning 작업의 ID
JOB_ID = "ftjob-bfaadc862e2c4e66834925fbb645ba80"

# Record the start time of the tracking
# 폴링 시작 시간 기록 (경과 시간 계산용)
start_time = time.time()

# Get the status of our fine-tuning job.
# 작업의 현재 상태 조회
ft_job = client.fine_tuning.jobs.retrieve(JOB_ID)
status = ft_job.status

# If the job isn't done yet, poll it every 30 seconds.
# 작업이 완료되지 않았으면 30초마다 상태 확인
while status not in ["succeeded", "failed"]:
    ft_job = client.fine_tuning.jobs.retrieve(JOB_ID)
    print(ft_job)
    status = ft_job.status

    # 경과 시간을 분과 초로 계산하여 표시
    print("Elapsed time: {} minutes {} seconds".format(
        int((time.time() - start_time) // 60),  # 분
        int((time.time() - start_time) % 60)))  # 초
    print(f'Status: {status}')

    # 화면을 지우고 다시 출력 (Jupyter Notebook에서 깔끔하게 표시)
    clear_output(wait=True)

    # 30초 대기 후 다시 확인
    time.sleep(30)
   
# 작업 완료 메시지 출력
print(f'Fine-tuning job {JOB_ID} finished with status: {status}')
