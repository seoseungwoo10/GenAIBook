# 모듈 설명: Stability AI 엔진 목록 조회 예제
# - Stability AI의 엔드포인트(/v1/engines/list)를 호출해 이용 가능한 엔진 목록을 가져옵니다.
# - 환경변수 STABILITY_API_KEY를 필요로 합니다.

# pip install stability-sdk

import os
import requests
import json

api_host = os.getenv('API_HOST', 'https://api.stability.ai')
url = f"{api_host}/v1/engines/list"

api_key = os.getenv("STABILITY_API_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.get(url, headers={
    "Authorization": f"Bearer {api_key}"
})

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
payload = response.json()

# format the payload for printing
payload = json.dumps(payload, indent=2)
print(payload)
