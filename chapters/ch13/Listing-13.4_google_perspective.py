# 모듈 설명: Listing 13.4 - Google Perspective API를 사용한 독성 탐지
# - 댓글, 사용자 입력 등의 독성(Toxicity)과 위협(Threat)을 탐지합니다.
# - 온라인 커뮤니티, 채팅, UGC(User Generated Content) 관리에 활용
# - Google의 머신러닝 모델로 유해 콘텐츠 자동 필터링
#
# 주요 개념:
# - Perspective API: Google Jigsaw의 독성 분석 API
# - Toxicity: 무례하거나 불쾌한 콘텐츠 (0-1 점수)
# - Threat: 위협적인 언어 탐지 (0-1 점수)
# - Threshold: 특정 점수 이상이면 조치 (예: 0.7 이상이면 차단)

# pip install google-api-python-client
import os
from googleapiclient import discovery
import json

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
SERVICE_URL = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1'

# Perspective API 클라이언트 생성
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=GOOGLE_API_KEY,
  discoveryServiceUrl=SERVICE_URL,
  static_discovery=False,
)

# 분석 요청 구성
analyze_request = {
  # 'comment': { 'text': 'Hello World - Greetings from the GenAI Book!' },  # 긍정적 예제
  'comment': { 'text': 'What kind of an idiot name is foo for a function' },  # 독성 있는 예제
  'requestedAttributes': {
    'TOXICITY': {},  # 독성 점수 요청
    'THREAT': {}     # 위협 점수 요청
  },
}

# API 호출 및 결과 분석
# 반환되는 점수:
# - summaryScore.value: 전체 독성/위협 점수 (0-1)
# - spanScores: 텍스트 부분별 점수
response = client.comments().analyze(body=analyze_request).execute()

# 결과 출력 (JSON 형식으로 보기 좋게 출력)
# "idiot" 같은 단어가 있으면 TOXICITY 점수가 높게 나옴
print(json.dumps(response, indent=2))

# 활용 예시:
# if response['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.7:
#     print("경고: 독성 콘텐츠가 감지되었습니다!")
#     # 댓글 차단, 경고 메시지 표시 등의 조치
