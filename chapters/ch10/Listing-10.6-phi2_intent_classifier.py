# 모듈 설명: Listing 10.6 - Phi-2 모델을 사용한 의도 분류(Intent Classification)
# - Microsoft의 소형 언어 모델 Phi-2를 사용하여 질문의 의도를 분류합니다.
# - 강아지 관련 질문인지 판별하여 적절한 처리 경로로 라우팅합니다.
# - 로컬에서 실행 가능한 작은 모델로 비용 절감 및 레이턴시 감소
#
# 주요 개념:
# - Phi-2: Microsoft의 2.7B 파라미터 소형 LLM (효율적이지만 성능 우수)
# - Intent Classification: 사용자 입력의 의도를 파악하는 NLP 태스크
# - Model Routing: 질문 유형에 따라 다른 모델/처리 경로 선택
# - Transformers: Hugging Face의 모델 로딩 및 추론 라이브러리

# We need to ensure the following packages are installed:
# pip install transformers==4.42.4 torch==2.3.1

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
import re
import logging

DEBUG = True

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

# Phi-2 모델 로드
# torch_dtype="auto": 자동으로 최적 데이터 타입 선택 (GPU 가용시 float16)
# trust_remote_code=True: 커스텀 모델 코드 실행 허용
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype="auto",
    trust_remote_code=True
)

# 토크나이저 로드 (텍스트를 토큰으로 변환)
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/phi-2",
    trust_remote_code=True
)

# Set the default device to CUDA if available, otherwise use CPU
# GPU가 있으면 사용, 없으면 CPU 사용
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Check if the question is about dogs
# 질문이 강아지에 관한 것인지 판별하는 함수
def check_dog_question(question):
    # 시스템 프롬프트: 강아지 관련 여부를 yes/no로 답변하도록 지시
    system_prompt = f"Instruct: Is there anything about dogs in the question below? If yes, answer with 'yes' else 'no'.\nQuestion:{question}\nOutput:"
    prompt = f"{system_prompt}\nUser:{question}\nOutput:"
    
    # 추론 실행 (그래디언트 계산 불필요)
    with torch.no_grad():
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            return_attention_mask=False,
            add_special_tokens=False
        )
        if DEBUG:
            print(f"Calling model with Inputs:{inputs}")

        # 입력을 모델이 있는 디바이스로 이동
        inputs = {name: tensor.to(model.device) for name, tensor in inputs.items()}

        # 텍스트 생성 (최대 500토큰)
        outputs = model.generate(
            **inputs,
            max_length=500,
            pad_token_id=tokenizer.eos_token_id
        )

    # 생성된 텍스트 디코딩
    text = tokenizer.batch_decode(outputs)[0]

    # Remove the prompt from the output text
    # 프롬프트 부분 제거 (답변만 남기기)
    text = text.replace(prompt, '').strip()
    text = text.replace("<|endoftext|>", '').strip()
    
    if DEBUG:
        print(f"Answer:{text}")

    # 정규식으로 "Output: Yes" 패턴 찾기
    regex = "^Output: Yes$"
    match = re.search(regex, text, re.MULTILINE)
    if match:
        if DEBUG:
            print("Found a match:", match.group())
        return True
    else:
        if DEBUG:
            print("No match found")
    
    return False

# Handle the user prompt
# 사용자 프롬프트에 대한 일반적인 응답 생성
def handle_prompt(user_input)->str:
    prompt = f"Instruct: Tell me more about this:{user_input}\nOutput:"

    with torch.no_grad():
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            return_attention_mask=False,
            add_special_tokens=False
        )
        inputs = {name: tensor.to(model.device) for name, tensor in inputs.items()}
        outputs = model.generate(
            **inputs,
            max_length=500,
            pad_token_id=tokenizer.eos_token_id
        )

    text = tokenizer.batch_decode(outputs)[0]

    # Remove the prompt from the output text
    text = text.replace(prompt, '').strip()
    text = text.replace("<|endoftext|>", '').strip()
    
    return text

# Handle the dog question
# 강아지 관련 질문을 처리 (RAG + GPT-4 호출 가능)
def handle_dog_question(question):
    # Handle the question using RAG and GPT4
    # This is a placeholder function, to show a proxy; we don't actually call the OpenAI model.
    # 실제로는 여기서 RAG 시스템 + GPT-4를 호출하여 답변 생성

    # Call OpenAI's GPT-4 to answer the question
    # Implement openai call here
    openai_response = f"This is a proxy to show that you are calling OpenAI's GPT-4 to answer the question: {question}"

    # 실제 구현 예시:
    # openai.api_key = "your-openai-api-key"
    # openai_response = openai.Completion.create(
    #   engine="gpt-4",
    #   prompt=f"Ask a question about dogs: {question}",
    #   max_tokens=400
    # )
    
    return openai_response
    
# Main function
if __name__=="__main__": 
    # Loop until the user enters "quit"
    while True:
        # Take user input
        user_prompt = input("What is your question (or type 'quit' to exit):")

        if user_prompt.casefold() == 'quit':
            break

        # 의도 분류: 강아지 관련 여부 판별
        if check_dog_question(user_prompt):
            # 강아지 관련 질문 -> 전문 RAG 시스템 사용
            print(handle_dog_question(user_prompt))
        else:
            # 일반 질문 -> 간단한 응답
            print("🤖 You did not ask about dogs")
            print("handle_prompt(user_prompt)")
    print("-" * 100)