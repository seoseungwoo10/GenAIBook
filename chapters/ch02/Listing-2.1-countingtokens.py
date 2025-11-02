"""
Listing 2.1 - 토큰 카운팅 예제
tiktoken 라이브러리를 사용하여 문자열의 토큰 개수를 세는 방법을 보여줍니다.
"""

import tiktoken as tk

def count_tokens(string: str, encoding_name: str) -> int:
    """
    주어진 문자열의 토큰 개수를 계산합니다.

    Args:
        string: 토큰 수를 셀 문자열
        encoding_name: 사용할 인코딩 이름 (예: "cl100k_base")

    Returns:
        토큰의 정수 개수
    """
    # 지정된 인코딩을 가져옴
    encoding = tk.get_encoding(encoding_name)
    
    # 문자열을 해당 인코딩으로 인코딩
    encoded_string = encoding.encode(string)

    # 인코딩된 토큰의 개수를 반환
    num_tokens = len(encoded_string)
    return num_tokens

# 입력 테스트 문자열
prompt = "I have a white dog named Champ"

# 문자열의 토큰 수 출력
# cl100k_base는 GPT-4 및 최신 모델에서 자주 사용되는 인코딩
print("Number of tokens:" , count_tokens(prompt, "cl100k_base"))
