# 모듈 설명: Listing 11.4 - MLflow를 사용한 LLM 관찰성(Observability)
# - MLflow로 LLM 애플리케이션의 메트릭, 파라미터, 로그를 추적합니다.
# - 토큰 사용량, 레이턴시, 대화 길이 등을 자동으로 기록
# - 실험 관리 및 성능 분석에 활용
#
# 주요 개념:
# - MLflow: ML 실험 추적 및 모델 관리 플랫폼
# - Observability: 시스템의 내부 상태를 외부에서 관찰 가능하게 만드는 것
# - Metrics: 레이턴시, 토큰 수 등 정량적 지표
# - Parameters: temperature, model 등 실험 설정값

import os
import time
import mlflow
from openai import OpenAI
import tiktoken as tk
from colorama import Fore, Style, init

# Set OpenAI API key
API_KEY = os.getenv("OPENAI_API_BOOK_KEY")
MODEL = "gpt-3.5-turbo"
MLFLOW_URI = "http://localhost:5000"  # MLflow 트래킹 서버 주소
TEMPERATURE = 0.7
TOP_P = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 800
DEBUG = False

# Initialize colorama
# 콘솔 출력에 색상 추가
init()

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Set MLflow tracking URI
# MLflow 서버 설정 및 실험 이름 지정
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment("GenAI_book")  # Replace with your experiment name

# Print user input and AI output with colors
# 사용자 입력과 AI 응답을 색상으로 구분하여 출력
def print_user_input(text):
    print(f"{Fore.GREEN}You: {Style.RESET_ALL}", text)

def print_ai_output(text):
    print(f"{Fore.BLUE}AI Assistant:{Style.RESET_ALL}", text)

# count tokens
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# Generate text using OpenAI API
# 텍스트 생성 및 메트릭 로깅
def generate_text(conversation, max_tokens=100)->str:
    # Generate text using OpenAI API
    start_time = time.time()
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY
    )
    latency = time.time() - start_time
    message_response = response.choices[0].message.content
    
    # Count tokens in the prompt and the completion
    # 프롬프트와 응답의 토큰 수 계산
    prompt_tokens = count_tokens(conversation[-1]['content'])
    conversation_tokens = count_tokens(str(conversation))
    completion_tokens = count_tokens(message_response)
    
    run = mlflow.active_run()
    if DEBUG:    
        print(f"Run ID: {run.info.run_id}")
        input("Press Enter to continue...")

    # MLflow에 메트릭 로깅
    # request_count: 요청 횟수
    # request_latency: 응답 시간
    # prompt_tokens: 프롬프트 토큰 수
    # completion_tokens: 응답 토큰 수
    # conversation_tokens: 전체 대화 토큰 수
    mlflow.log_metrics({
        "request_count": 1,
        "request_latency": latency,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "conversation_tokens": conversation_tokens
    })
    
    # MLflow에 파라미터 로깅
    # 실험 재현을 위한 설정값 기록
    mlflow.log_params({
        "model": MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "frequency_penalty": FREQUENCY_PENALTY,
        "presence_penalty": PRESENCE_PENALTY
    })

    return message_response
        
if __name__ == "__main__":
    # MLflow 자동 로깅 활성화
    mlflow.autolog()

    # Start a new MLflow run
    # MLflow 실행 시작 (모든 메트릭과 파라미터가 이 run에 기록됨)
    with mlflow.start_run() as run:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit", "q", "e"]:
                break

            conversation.append({"role": "user", "content": user_input})
            ai_output = generate_text(conversation, MAX_TOKENS)
            print_ai_output(ai_output)
            conversation.append({"role": "assistant", "content": ai_output})
