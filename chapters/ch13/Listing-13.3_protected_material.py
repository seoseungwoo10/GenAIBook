# 모듈 설명: Listing 13.3 - Azure Content Safety의 보호된 자료 탐지
# - 저작권으로 보호되는 노래 가사, 뉴스 기사 등을 감지합니다.
# - LLM이 저작권 침해 콘텐츠를 생성하는 것을 방지
# - 법적 리스크 완화 및 윤리적 AI 사용을 위한 필수 기능
#
# 주요 개념:
# - Protected Material: 저작권, 특허 등으로 보호되는 콘텐츠
# - Copyright Infringement: 저작권 침해 리스크
# - Detection: 보호된 자료의 존재 여부 및 유사도 확인

import requests
import os
import http.client

CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("CONTENT_SAFETY_KEY")
API_VERSION = "2023-10-15-preview"

# 테스트용 텍스트: Taylor Swift의 "Mastermind" 가사 일부
# 이 텍스트는 저작권으로 보호되므로 API가 탐지함
text_to_analyze = "Once upon a time The planets and the fates and all the stars aligned You and I ended up in the same room at the same time And the touch of a hand lit the fuse Of a chain reaction of countermoves To assess the equation of you Checkmate, I couldn't lose What if I told you none of it was accidental? And the first night that you saw me Nothing was gonna stop me I laid the groundwork, and then just like clockwork The dominoes cascaded in a line What if I told you I'm a mastermind? And now you're mineIt was all by design 'Cause I'm a mastermind You see, all the wisest women had to do it this way 'Cause we were born to be the pawn in every lover's game If you fail to plan, you plan to fail Strategy sets the scene for the tale I'm the wind in our free-flowing sails And the liquor in our cocktails What if I told you none of it was accidental"

# Set up the API request
url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:detectProtectedMaterial?api-version={API_VERSION}"

headers = {
  "Content-Type": "application/json",
  "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY
}
data = {
  "text": text_to_analyze
}

# Send the API request
# Protected Material Detection API 호출
response = requests.post(url, headers=headers, json=data, timeout=10)

# Handle the API response
# 결과에는 탐지 여부, 신뢰도, 매칭된 보호 자료 정보 등이 포함됨
if response.status_code == 200:
    result = response.json()
    print("Analysis result:", result)
    # 예상 결과: 저작권 보호 가사로 탐지됨
else:
    print("Error:", response.status_code, response.text)