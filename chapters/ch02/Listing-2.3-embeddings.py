"""
Listing 2.3 - 텍스트 임베딩 생성 예제
OpenAI의 임베딩 API를 사용하여 텍스트를 벡터로 변환하는 방법을 보여줍니다.
임베딩은 의미적 유사성 검색, 클러스터링, 분류 등에 사용됩니다.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수(.env) 로드
load_dotenv()

# OpenAI 클라이언트 초기화 (환경변수 OPENAI_API_KEY 필요)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    """
    주어진 텍스트의 임베딩 벡터를 반환합니다.

    Args:
        text: 임베딩을 생성할 문자열

    Returns:
        임베딩 벡터 (예: 1536차원 리스트)
    """
    # text-embedding-ada-002 모델을 사용해 임베딩 생성
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text)
    # 첫 번째 결과의 embedding 반환
    return response.data[0].embedding

# 샘플 텍스트의 임베딩 생성 및 길이/일부 값 출력
embeddings = get_embedding("I have a white dog named Champ.")
print("Embedding Length:", len(embeddings))
print("Embedding:", embeddings[:5])
