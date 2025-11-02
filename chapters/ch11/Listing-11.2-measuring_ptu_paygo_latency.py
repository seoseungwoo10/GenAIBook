# 모듈 설명: Listing 11.2 - PTU vs Pay-As-You-Go 레이턴시 비교 측정
# - PTU(Provisioned Throughput Units)와 PAYGO(종량제) 배포 방식의 성능을 비교합니다.
# - 동일한 조건에서 두 배포 방식의 응답 시간을 측정하여 비용 대비 성능 분석
#
# 주요 개념:
# - PTU: 고정 용량 예약 방식 (예측 가능한 성능, 고정 비용)
# - PAYGO: 사용량 기반 과금 (변동 비용, 트래픽 급증 시 throttling 가능)
# - Latency: API 응답까지 걸리는 시간 (낮을수록 좋음)
# - Throughput: 단위 시간당 처리 가능한 요청 수

import os
import logging
import random
import time
from tqdm import tqdm
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Set up logging
# 로그를 파일에 저장하여 분석
logging.basicConfig(filename='aoai_ptu.log', level=logging.INFO)

# Define constants
LOAD_TEST_ITERATIONS = 10

# Azure OpenAI Chat API endpoint and API key
# PTU 배포용 엔드포인트 및 키
AOAI_PTU_KEY = os.getenv("AOAI_PTU_KEY")
AOAI_PTU_ENDPOINT = os.getenv("AOAI_PTU_ENDPOINT")
API_VERSION = "2024-02-15-preview"
PTU_MODEL = "demo-sb"

# Pay-As-You-Go 배포용 엔드포인트 및 키
AOAI_PAYGO_KEY = os.getenv("AOAI_KEY")
AOAI_PAYGO_ENDPOINT = os.getenv("AOAI_ENDPOINT")
PAYGO_MODEL = "gp4"

TEMPERATURE = 0.75
MAX_TOKENS = 256
NUM_INTERATION = 100  # 각 배포에서 100회 요청 실행
DEBUG = False

# Initialize Azure OpenAI clients
# PTU와 PAYGO 각각의 클라이언트 초기화
ptu_client = AzureOpenAI(
    azure_endpoint=AOAI_PTU_ENDPOINT,
    api_key=AOAI_PTU_KEY,
    api_version=API_VERSION
)

paygo_client = AzureOpenAI(
    azure_endpoint=AOAI_PAYGO_ENDPOINT,
    api_key=AOAI_PAYGO_KEY,
    api_version=API_VERSION
)

# Test inputs
# 다양한 질문으로 실제 사용 시나리오 시뮬레이션
test_inputs = [
    "Hello",
    "How are you?",
    "What's the capital of Hawaii?",
    "Tell me a dad joke",
    "Tell me a story",
    "What's your favorite movie?",
    "What's the meaning of life?",
    "What's the capital of India?",
    "What's the square root of 1976?",
    "What's the largest mammal?",
    f"Write a story about a Panda F1 driver in less than {MAX_TOKENS} words"
]

# Function to call the Azure OpenAI Chat API and measure latency
# API 호출 및 레이턴시 측정
def call_completion_api(client, model, user_input):
    conversation = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_input}
    ]
    
    try:
        # 시작 시간 기록
        start_time = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        # 레이턴시 계산
        latency = time.time() - start_time
        
        message_response = response.choices[0].message.content
        token_count = response.usage.completion_tokens
        
        if DEBUG:
            logging.info("AI Assistant: %s", message_response)
        return latency, token_count
    except Exception as e:
        logging.error("Error calling API: %s", str(e))
        return None, None

# Main function to run the load test
# 부하 테스트 실행 (PTU와 PAYGO 순차적으로 테스트)
def main():
    # PTU와 PAYGO 각각 테스트
    for client, model, test_name in [
        (ptu_client, PTU_MODEL, "PTU"),
        (paygo_client, PAYGO_MODEL, "PAYGO")
    ]:
        print(f"Starting {test_name} test...")

        # ThreadPoolExecutor로 병렬 요청 실행
        with ThreadPoolExecutor(max_workers=20) as executor:
            latencies = []
            # 랜덤하게 질문 선택하여 100개 요청 생성
            futures = [
                executor.submit(call_completion_api, client, model, input)
                for input in random.choices(test_inputs, k=NUM_INTERATION)
            ]

            # 진행 상황 표시하며 결과 수집
            for future in tqdm(as_completed(futures), total=NUM_INTERATION):
                latency, token_count = future.result()
                if latency is not None and token_count is not None:
                    logging.info(f"Latency: {latency}s, Token Count: {token_count}")
                    latencies.append(latency)
        
        # Calculate and print metrics
        # 통계 계산 및 출력
        average_latency = sum(latencies) / len(latencies) if latencies else None
        min_latency = min(latencies) if latencies else None
        max_latency = max(latencies) if latencies else None
        median_latency = statistics.median(latencies) if latencies else None
        
        print(f"Median Latency: {median_latency}s")
        print(f"Average Latency: {average_latency}s")
        print(f"Min Latency: {min_latency}s")
        print(f"Max Latency: {max_latency}s")
    
if __name__ == "__main__":
    main()