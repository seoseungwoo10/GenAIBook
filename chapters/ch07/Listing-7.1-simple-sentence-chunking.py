# 모듈 설명: Listing 7.1 - 간단한 문장 단위 청킹 및 임베딩 생성
# - 정규식으로 텍스트를 문장 단위로 분할하고 각 문장의 임베딩 벡터를 생성합니다.
# - RAG(Retrieval-Augmented Generation) 시스템의 기본 구성 요소
#
# 주요 개념:
# - Text Chunking: 긴 문서를 작은 단위로 분할 (토큰 제한 대응)
# - Sentence Splitting: 문장 단위로 분할 (.!?를 기준)
# - Embeddings: 텍스트의 의미를 벡터로 표현 (유사도 검색에 사용)
# - tiktoken: OpenAI의 토큰 카운팅 라이브러리

import os
import re
from openai import OpenAI
from tqdm import tqdm # for progress bars
import tiktoken as tk

# Initialize the OpenAI client
# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# function that splits the text into chunks based on sentences
# 정규식으로 문장 단위로 텍스트 분할 (.!?를 기준으로)
# 장점: 빠르고 간단
# 단점: "Mr.", "Dr." 같은 약어에서 오분할 가능
def split_sentences(text):
    sentences = re.split('[.!?]', text)  # 문장 종결 부호로 분할
    sentences = [sentence.strip() for sentence in sentences if sentence]  # 공백 제거
    return sentences

# count tokens
# tiktoken을 사용해 문자열의 토큰 수 계산
# 토큰 수는 API 비용과 직결되므로 정확한 카운팅 필요
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    # cl100k_base: GPT-3.5-turbo, GPT-4 사용
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    # 문자열을 토큰 ID 리스트로 변환
    encoded_string = encoding.encode(string)

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# OpenAI embeddings example from Chapter 2
# 주어진 텍스트의 임베딩 벡터를 생성
# text-embedding-ada-002: OpenAI의 최신 임베딩 모델 (1536차원)
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",  # 임베딩 모델
        input=text)  # 임베딩할 텍스트
    return response.data[0].embedding  # 1536차원 벡터 반환

if __name__ == "__main__":
    # Example usage:
    # 예제 텍스트 (4개 문장)
    text = "This is the first sentence. This is the second sentence. Guess what? This is the fourth sentence."

    # 텍스트를 문장으로 분할
    sentences = split_sentences(text)

    # Initialize an empty 2D array
    # 문장과 임베딩을 저장할 2D 배열
    sentence_embeddings = []
    total_token_count = 0

    # 각 문장에 대해 토큰 수 계산 및 임베딩 생성
    for sentence in tqdm(sentences):
        # Count the number of tokens in the sentence
        # 각 문장의 토큰 수 계산 (비용 추정용)
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        # 문장의 임베딩 벡터 생성
        embedding = get_embedding(sentence)
        # [문장, 임베딩] 쌍으로 저장
        sentence_embeddings.append([sentence, embedding])

    # Now, sentence_embeddings is a 2D array where each element is a list of the form [sentence, embedding]
    # 결과: [[문장1, 벡터1], [문장2, 벡터2], ...]
    print("Number of sentence embeddings:", len(sentence_embeddings))
    print("Total number of tokens:", total_token_count)