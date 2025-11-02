"""
Listing 2.2 - 인코딩/디코딩 예제
- tiktoken을 사용해 문자열을 토큰으로 인코딩하고, 토큰을 다시 문자열로 디코딩하는 예시를 제공합니다.
- 여러 인코딩 방식(cl100k_base, p50k_base, r50k_base)을 비교합니다.
"""

import tiktoken as tk

def get_tokens(string: str, encoding_name: str) -> str:
    """
    문자열을 주어진 인코딩으로 인코딩하여 토큰 리스트(또는 토큰 배열)를 반환합니다.

    Args:
        string: 인코딩할 문자열
        encoding_name: 사용할 인코딩 이름

    Returns:
        인코딩된 토큰 리스트
    """
    # 지정된 인코딩 객체 가져오기
    encoding = tk.get_encoding(encoding_name)
    
    # 문자열을 인코딩하여 토큰 리스트 반환
    return encoding.encode(string)

def get_string(tokens: str, encoding_name: str) -> str:
    """
    토큰 리스트를 주어진 인코딩으로 디코딩하여 원래 문자열로 복원합니다.

    Args:
        tokens: 디코딩할 토큰 리스트
        encoding_name: 사용할 인코딩 이름

    Returns:
        디코딩된 문자열
    """
    # 지정된 인코딩 객체 가져오기
    encoding = tk.get_encoding(encoding_name)
    
    # 토큰을 디코딩하여 문자열로 반환
    return encoding.decode(tokens)


# 테스트용 입력 문자열
prompt = "I have a white dog named Champ."

# 다양한 인코딩으로 토큰화 결과를 출력
# cl100k_base: GPT-4 및 최신 모델에서 사용
print("cl100k_base Tokens:" , get_tokens(prompt, "cl100k_base"))
# p50k_base: Codex 및 일부 GPT-3 모델에서 사용
print("  p50k_base Tokens:" , get_tokens(prompt, "p50k_base"))
# r50k_base: 초기 GPT-3 모델에서 사용
print("  r50k_base Tokens:" , get_tokens(prompt, "r50k_base"))


# 토큰 배열을 다시 문자열로 디코딩하는 예
# 예시 토큰: [40, 617, 264, 4251, 5679, 7086, 56690, 13]
print("Original String:" , get_string([40, 617, 264, 4251, 5679, 7086, 56690], "cl100k_base"))