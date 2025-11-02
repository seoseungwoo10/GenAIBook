# 모듈 설명: Listing 10.5 - LlamaIndex를 사용한 문서 Q&A 시스템
# - LlamaIndex(구 GPT Index) 프레임워크를 사용한 RAG 시스템 구축
# - PDF 문서를 자동으로 인덱싱하고 영구 저장소에 저장
# - 인덱스가 이미 존재하면 재사용하여 시간 절약
#
# LlamaIndex 주요 개념:
# - VectorStoreIndex: 문서를 벡터로 변환하여 저장하는 인덱스
# - SimpleDirectoryReader: 디렉토리의 모든 문서를 자동으로 로드
# - StorageContext: 인덱스의 영구 저장 관리
# - QueryEngine: 자연어 질의를 처리하는 엔진

# Name: llama-index
# Version: 0.10.9
# Summary: Interface between LLMs and your data
# Home-page: https://llamaindex.ai

#pip install llama-index==0.10.9
# pip install llama-index-readers-file

import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.readers.file import PDFReader

PERSIST_DIR = "./storage/llamaindex"  # 인덱스 저장 디렉토리
DOG_BOOKS = "./data/dog_books/"
#DOG_BOOKS = "./data/dog_books_test/" #Used for testing with one file
DEBUG = True

# Load environment variables
load_dotenv('.env')
OPENAI_KEY = os.getenv('OPENAI_API_BOOK_KEY')

# 전역 설정: 임베딩 모델 지정
Settings.embed_model = OpenAIEmbedding(api_key=OPENAI_KEY)

# Load or create the index
# 기존 인덱스 로드 또는 새로 생성
def load_or_create_index():
    # check if storage already exists
    # 저장된 인덱스가 없으면 새로 생성
    if not os.path.exists(PERSIST_DIR):
        try:
            print("Loading PDFs from ", DOG_BOOKS)
            parser = PDFReader()
            file_extractor = {".pdf": parser}
            
            # load the documents and create the index
            # SimpleDirectoryReader: 디렉토리의 모든 PDF 자동 로드
            required_exts = [".pdf"]
            documents = SimpleDirectoryReader(
                DOG_BOOKS,
                file_extractor=file_extractor,
                required_exts=required_exts
            ).load_data()

            print("Loaded ", len(documents), "documents.")

            # VectorStoreIndex: 문서를 임베딩으로 변환하여 인덱스 생성
            # show_progress=True: 진행 상황 표시
            index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True
            )

            # store it for later
            # 인덱스를 디스크에 저장 (다음 실행 시 재사용)
            index.storage_context.persist(persist_dir=PERSIST_DIR)
            
            print("Index created and stored in", PERSIST_DIR)
        except Exception as e:
            print("Error while creating index:", e)
            exit()
    else:
        # 기존 인덱스 로드
        print("Loading existing index from", PERSIST_DIR)
        
        try:
            # load the existing index
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
        except Exception as e:
            print("Error while loading index:", e)
            exit()
    return index

# Check if user wants to quit
def check_prompt(user_input):
    user_input = user_input.strip().lower()
    if user_input.casefold() == 'exit' or user_input.casefold() == 'quit':
        exit()
    return user_input

# Main loop
def main():
    # 인덱스 로드 또는 생성
    index = load_or_create_index()

    # QueryEngine: 질의 처리 엔진 생성
    # 내부적으로 벡터 검색 + LLM 답변 생성 수행
    query_engine = index.as_query_engine()

    while True:
        prompt = check_prompt(input("Ask a question about dogs:"))
        if not prompt:
            print("Please enter a valid question.")
            continue

        # query: 질문을 처리하여 답변 반환
        # LlamaIndex가 자동으로 관련 문서를 찾아 LLM에 전달
        response = query_engine.query(prompt)
        print(response)
        
if __name__ == "__main__":
    main()