# 모듈 설명: Listing 11.7 - Redis를 사용한 의미적 캐싱(Semantic Caching)
# - 유사한 질문에 대해 이전 응답을 재사용하여 비용 절감 및 속도 향상
# - 벡터 유사도 기반 캐싱으로 완전히 동일하지 않아도 캐시 히트 가능
# - RedisVL의 SemanticCache를 사용한 구현
#
# 주요 개념:
# - Semantic Cache: 의미적으로 유사한 쿼리를 감지하여 캐시 재사용
# - Distance Threshold: 유사도 임계값 (0.1 = 매우 유사해야 캐시 히트)
# - Cache Hit: 캐시에서 찾아서 반환 (빠름, 비용 없음)
# - Cache Miss: 캐시에 없어서 LLM 호출 필요 (느림, 비용 발생)

# pip install redisvl

# Check if it is running
# look at the index specification created for the semantic cache lookup
# !rvl index info -i llmcache

import os
import time
from openai import AzureOpenAI
from redisvl.extensions.llmcache import SemanticCache
import numpy as np
import random

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

MODEL = "gp4"
TEMPERATURE = 0.75
TOP_P = 0.95
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 25
DEBUG = True

def initialize_cache():
    # Initialize the semantic cache
    # SemanticCache 초기화
    llmcache = SemanticCache(
        name="GenAIBookCache",                # Redis 인덱스 이름
        prefix="bookcache",                   # redis key-prefix for hash entries
        redis_url="redis://localhost:6379",   # Redis 연결 URL
        distance_threshold=0.1                # semantic cache distance threshold
                                              # 0.1: 매우 유사한 질문만 캐시 히트
                                              # 값이 클수록 더 관대하게 캐시 히트
    )
    return llmcache

# Initialize OpenAI client
client = AzureOpenAI(
  azure_endpoint = AZURE_ENDPOINT, 
  api_key=AOAI_API_KEY,  
  api_version=API_VERSION
)

# Define a list of questions
# 테스트용 질문 목록
input_questions = [
    "What is the capital of UK?",
    "What is the capital of France?",
    "What's the square root of 144?",
    "What is the capital of WA state?",
    "What is the capital of USA?",
    "What is the capital of Canada?",
    "What is the capital of Australia?",
    "What is the capital of India?",
    "What is the capital of China?",
    "What is the capital of Japan?"
]

# Generate response using OpenAI API
# OpenAI API를 직접 호출하여 응답 생성
def generate_response(conversation, max_tokens=25)->str:
    response = client.chat.completions.create(
        model=MODEL,
        messages = conversation,
        temperature = TEMPERATURE,
        max_tokens = max_tokens,
    )
    return response.choices[0].message.content

# Function to answer a question using the cache
# 캐시를 사용하여 질문에 답변
def answer_question(question: str) -> str:
    conversation = [{"role": "assistant", "content": question}]
    
    # 캐시에서 유사한 질문 찾기
    results = llmcache.check(prompt=question)
    if results:
        # Cache Hit: 이전 응답 재사용
        answer = results[0]["response"]
        if DEBUG:
            print(f"Cache hit for prompt: {question}, answer: {answer}")
    else:
        # Cache Miss: LLM 호출 후 캐시에 저장
        answer = generate_response(conversation)
        llmcache.store(prompt=question, response=answer)
        if DEBUG:
            print(f"Cache miss for prompt: {question}, added to cache with response: {answer}")
    
    return answer

if __name__ == "__main__":
    llmcache = initialize_cache()

    times_without_cache = []
    times_with_cache = []

    # 각 질문에 대해 캐시 사용/미사용 시간 측정
    for question in input_questions:
        # Without caching
        # 캐시 없이 매번 LLM 호출
        start_time = time.time()
        answer = generate_response([{"role": "assistant", "content": question}])
        end_time = time.time()
        times_without_cache.append(end_time-start_time)

        # With caching
        # 캐시 사용 (두 번째 실행부터 캐시 히트)
        start_time = time.time()
        answer = answer_question(question)
        end_time = time.time()
        times_with_cache.append(end_time-start_time)

    # 성능 비교 통계 출력
    avg_time_without_cache = np.mean(times_without_cache)
    avg_time_with_cache = np.mean(times_with_cache)

    print(f"Avg time taken without cache: {avg_time_without_cache}")
    print(f"Avg time taken with LLM cache enabled: {avg_time_with_cache}")
    print(f"Percentage of time saved: {round((avg_time_without_cache - avg_time_with_cache) / avg_time_without_cache * 100, 2)}%")