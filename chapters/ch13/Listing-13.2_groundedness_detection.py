# 모듈 설명: Listing 13.2 - Azure Content Safety의 근거 탐지(Groundedness Detection)
# - AI 생성 텍스트가 제공된 소스 문서에 근거하고 있는지 검증합니다.
# - 환각(Hallucination) 탐지에 사용되며, RAG 시스템의 신뢰성 향상에 필수적
# - 의료, 법률 등 사실 정확성이 중요한 도메인에서 특히 중요
#
# 주요 개념:
# - Groundedness: 생성된 텍스트가 원본 문서에 기반하고 있는 정도
# - Hallucination: LLM이 사실이 아닌 내용을 그럴듯하게 생성하는 현상
# - Domain: 평가 도메인 지정 (Medical, Generic 등)
# - Task: 평가 태스크 유형 (Summarization, QnA 등)
# - Reasoning: 상세한 이유 반환 여부

import requests
import os
from dotenv import load_dotenv

# Set the API endpoint and key
CONTENT_SAFETY_KEY = os.getenv("CONTENT_SAFETY_KEY")
CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
API_VERSION = "2024-02-15-preview"

# Build the request payload
# 근거 탐지 요청 페이로드 구성
payload = {
    "domain": "Medical",  # 평가 도메인 (의료 분야)
    "task": "Summarization",  # 태스크 유형 (요약)
    "text": "Ms Johnson has been in the hospital after experiencing a stroke.",  # 검증할 텍스트
    "groundingSources": [  # 근거가 되는 원본 문서
        "Our patient, Ms. Johnson, presented with persistent fatigue, unexplained weight loss, and frequent night sweats. After a series of tests, she was diagnosed with Hodgkin's lymphoma, a type of cancer that affects the lymphatic system. The diagnosis was confirmed through a lymph node biopsy revealing the presence of Reed-Sternberg cells, a characteristic of this disease. She was further staged using PET-CT scans. Her treatment plan includes chemotherapy and possibly radiation therapy, depending on her response to treatment. The medical team remains optimistic about her prognosis given the high cure rate of Hodgkin's lymphoma."
    ],
    "reasoning": False  # True시 상세한 설명 포함
}

headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY
}

# Send the API request
# Groundedness Detection API 호출
url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:detectGroundedness?api-version={API_VERSION}"
response = requests.post(url, headers=headers, json=payload, timeout=10)

# 결과 처리
# 원본 문서와 생성 텍스트의 일치성 확인
# 이 예제에서는 "stroke"가 원문에 없으므로 ungrounded로 탐지됨
if response.status_code == 200:
    result = response.json()
    print("detectGroundedness result:", result)
else:
    print("Error:", response.status_code, response.text)
