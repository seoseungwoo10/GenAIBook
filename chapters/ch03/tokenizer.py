# 모듈 설명: 토크나이저 예제 - tiktoken을 사용한 토큰화
# - OpenAI의 tiktoken 라이브러리로 텍스트를 토큰으로 변환합니다.
# - 토큰은 모델이 이해하는 기본 단위 (단어, 하위단어, 문자 조합)
#
# 주요 개념:
# - Tokenization: 텍스트를 모델이 처리할 수 있는 숫자 ID로 변환
# - tiktoken: OpenAI의 공식 토크나이저 라이브러리 (빠르고 정확)
# - p50k_base: GPT-3 모델에 사용되는 인코딩 방식
# - 다른 인코딩: cl100k_base (GPT-4, GPT-3.5-turbo), r50k_base 등

import tiktoken as tk

def get_tokens(string: str) -> str:
    """
    주어진 문자열을 토큰 ID 리스트로 변환합니다.

    Args:
        string: 토큰화할 텍스트

    Returns:
        토큰 ID의 리스트 (예: [47, 333, 1234])
    """
    # p50k_base 인코딩 가져오기 (GPT-3용)
    # GPT-3.5-turbo/GPT-4는 cl100k_base 사용
    encoding = tk.get_encoding("p50k_base")
    
    # 문자열을 토큰 ID 리스트로 인코딩
    # 예: "Hello" -> [15496]
    return encoding.encode(string)
  
# 테스트할 텍스트 배열
# 같은 단어도 대소문자에 따라 다른 토큰으로 인식될 수 있음
texts = ["Purr Purrs Meow Purr purr purrs meow"]

for text in texts:  
    # 토큰화 수행
    tokenized_text = get_tokens(text)
  
    # 원문과 토큰 ID 리스트 출력
    # 각 단어가 어떻게 토큰화되는지 확인
    print(f"'{text}:{tokenized_text}'")
